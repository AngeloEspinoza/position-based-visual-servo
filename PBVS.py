import cv2
import cv2.aruco as aruco
import numpy as np
import rotm2euler
import matplotlib.pyplot as plt
import math
import os

def draw_axis(img, corners, img_pts):
    corner = tuple(corners[0].ravel().astype(int))
    cv2.line(img, corner, tuple(img_pts[0].ravel().astype(int)), (0, 0, 255), 3)
    cv2.line(img, corner, tuple(img_pts[1].ravel().astype(int)), (0, 255, 0), 3)
    cv2.line(img, corner, tuple(img_pts[2].ravel().astype(int)), (255, 0, 0), 3)

MARKER_SIZE = 95 # milimeters
BLUE = (255, 0, 0)

# Read intrinsic parameters of the camera
with np.load('camera_matrix.npz') as X:
	K, dist, rvecs, tvecs = [X[i] for i in ('camera_matrix',
											'dist',
											'rvecs',
											'tvecs')]

# Define the 4X4 bit ArUco tag
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

# Define camera to use and set resolution and frame rate
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

# Define coordinates in object coordinate space (3D space)
obj_points = np.zeros((5, 3), np.float32)
obj_points[1, 0], obj_points[1, 1], obj_points[2, 0] = -MARKER_SIZE / 2, -MARKER_SIZE / 2, MARKER_SIZE / 2
obj_points[2, 1], obj_points[3, 0], obj_points[3, 1] = -MARKER_SIZE / 2, MARKER_SIZE / 2, MARKER_SIZE / 2
obj_points[4, 0], obj_points[4, 1] = -MARKER_SIZE / 2, MARKER_SIZE / 2

# 3D axis coordinates to be drawn on the ArUco marker 
axis = np.float32([[45, 0, 0], [0, -45, 0], [0, 0, -45]]).reshape(-1, 3)

estimated_pose = np.identity(n=4, dtype=np.float64) # Estimated pose matrix
desired_pose = np.identity(n=4, dtype=np.float64) # Desired pose matrix

while True:
	# Read frames of the camera
	ret, frame = cap.read()

	# Convert image to gray scale
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	corners, ids, rejected = aruco.detectMarkers(frame_gray, 
												 ARUCO_DICT,
												 K,
												 dist)
	
	# Verify at least one ArUco marker was detected
	if len(corners) > 0 or ids is not None:
		try:
			desired_pose = np.load('desired_pose.npy')
			desired_realworld_tvec = np.load('desired_realworld_tvec.npy')
			desired_euler_angles = np.load('desired_euler_angles.npy')
		except FileNotFoundError:
			print('[INFO]: FileNotFoundError handled, check if all .npy files were loaded')
			pass

		aruco.drawDetectedMarkers(frame, corners)

		# Center point between the 4 corners
		aruco_center = np.asarray((abs(corners[0][0][2][0] + corners[0][0][0][0]) // 2,
							       abs(corners[0][0][2][1] + corners[0][0][0][1]) // 2)).astype(int)
		
		# Array with the center of the ArUco marker
		new_corners = np.array([np.vstack((aruco_center, corners[0][0]))])

		# Draw axis and corners of the markers
		for marker in range(len(ids)):
			for corner in range(4):
				try:
					# Find the rotation and translation vectors
					_, rvec, tvec = cv2.solvePnP(obj_points, new_corners[marker],
				    							 K, dist)

					corner_x, corner_y = corners[marker][0, corner]
					center_coordinates = tuple((int(corner_x), int(corner_y)))

					cv2.circle(frame, center_coordinates, 3, BLUE, -1)
					cv2.circle(frame, aruco_center, 3, BLUE, -1)

					corner_xy_str = '({0}, {1})'.format(corner_x, corner_y)
					cv2.putText(frame, corner_xy_str, center_coordinates, 
								cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 
								1, cv2.LINE_AA)

					img_pts, jac = cv2.projectPoints(axis, rvec, tvec, K, dist)
					draw_axis(frame, new_corners[marker], img_pts)

					rvec_flipped = -rvec.ravel()
					tvec_flipped = -tvec.ravel()

					# Convert rvec to a rotation matrix, and then to a Euler angles
					R, jacobian = cv2.Rodrigues(rvec_flipped)
					
					# From image plane to world coordinates
					realworld_tvec = np.dot(R, tvec_flipped)
					realworld_tvec[1], realworld_tvec[2] = -realworld_tvec[1], -realworld_tvec[2]
					
					# Conversion euler angles in radians, and then to degrees
					pitch, roll, yaw =  rotm2euler.rotation_matrix_to_euler_angles(R)
					pitch, roll, yaw = math.degrees(pitch), math.degrees(roll), math.degrees(yaw)
					estimated_euler_angles = np.array([roll, pitch, yaw])

					# Construct homogeneous transformation matrix
					estimated_pose[:3, :3] = R
					estimated_pose[:3, 3] = realworld_tvec
				except IndexError:
					print('[INFO]: IndexError handled')
					pass
				continue
		
		desired_realworld_tvec_str_x = 'Desired translation vector x: {}'.format(desired_realworld_tvec[0])
		desired_realworld_tvec_str_y = 'Desired translation vector y: {}'.format(desired_realworld_tvec[1])
		desired_realworld_tvec_str_z = 'Desired translation vector z: {}'.format(desired_realworld_tvec[2])
							
		tvec_error_str_x ='Translation error x: {}'.format(realworld_tvec[0] - desired_realworld_tvec[0])
		tvec_error_str_y ='Translation error y: {}'.format(realworld_tvec[1] - desired_realworld_tvec[1])
		tvec_error_str_z ='Translation error z: {}'.format(realworld_tvec[2] - desired_realworld_tvec[2])

		desired_euler_angles_str_roll = 'Desired euler angle roll: {}'.format(desired_euler_angles[0])
		desired_euler_angles_str_pitch = 'Desired euler angle pitch: {}'.format(desired_euler_angles[1])
		desired_euler_angles_str_yaw = 'Desired euler angle yaw: {}'.format(desired_euler_angles[2])

		rvec_error_str_roll ='Rotation error roll: {}'.format(estimated_euler_angles[0] - desired_euler_angles[0])
		rvec_error_str_pitch ='Rotation error pitch: {}'.format(estimated_euler_angles[1] - desired_euler_angles[1])
		rvec_error_str_yaw ='Rotation error yaw: {}'.format(estimated_euler_angles[2] - desired_euler_angles[2])

		tvec_str_x = 'x = {0:4.0f} milimiters'.format(realworld_tvec[0])
		tvec_str_y = 'y = {0:4.0f} milimiters'.format(realworld_tvec[1])
		tvec_str_z = 'z = {0:4.0f} milimiters'.format(realworld_tvec[2])

		rvec_str_pitch = 'pitch = {0:4.0f} degrees'.format(pitch)
		rvec_str_roll = 'roll = {0:4.0f} degrees'.format(roll)
		rvec_str_yaw = 'yaw = {0:4.0f} degrees'.format(yaw)

		cv2.putText(frame, desired_realworld_tvec_str_x, (300, 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, desired_realworld_tvec_str_y, (300, 20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, desired_realworld_tvec_str_z, (300, 30), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		
		cv2.putText(frame, tvec_error_str_x, (300, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_error_str_y, (300, 60), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_error_str_z, (300, 70), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

		cv2.putText(frame, desired_euler_angles_str_roll, (300, 90), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, desired_euler_angles_str_pitch, (300, 100), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, desired_euler_angles_str_yaw, (300, 110), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		
		cv2.putText(frame, rvec_error_str_roll, (300, 130), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, rvec_error_str_pitch, (300, 140), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, rvec_error_str_yaw, (300, 150), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

		cv2.putText(frame, tvec_str_x, (5, 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_str_y, (5, 20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_str_z, (5, 30), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

		cv2.putText(frame, rvec_str_roll, (5, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, rvec_str_pitch, (5, 60), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, rvec_str_yaw, (5, 70), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		
	cv2.imshow('PVBS - RGB', frame)

	# If 'q' pressed, save the current pose of the ArUco marker 
	if cv2.waitKey(1) & 0xFF == ord('q'):
		desired_pose = estimated_pose
		desired_euler_angles = estimated_euler_angles
		desired_realworld_tvec = realworld_tvec

		np.save('desired_pose.npy', desired_pose)
		np.save('desired_euler_angles.npy', desired_euler_angles)
		np.save('desired_realworld_tvec.npy', desired_realworld_tvec)

		print('[INFO]: ArUco marker pose saved')

	# If ESC pressed exit
	if cv2.waitKey(1) & 0xFF == 27:
		break

# Close all 
cap.release()
cv2.destroyAllWindows()