import cv2
import cv2.aruco as aruco
import numpy as np
import rotm2euler
import matplotlib.pyplot as plt
import math
import os
import time
import GUI

def draw_axis(img, start_pts, img_pts):
    start_point = list(start_pts[0].ravel().astype(int))
    end_point_x = list(img_pts[0].ravel().astype(int))
    end_point_y = list(img_pts[1].ravel().astype(int))
    end_point_z = list(img_pts[2].ravel().astype(int))

    cv2.arrowedLine(img, start_point, end_point_x, RED, 2)
    cv2.arrowedLine(img, start_point, end_point_y, GREEN, 2)
    cv2.arrowedLine(img, start_point, end_point_z, BLUE, 2)

    end_point_x[0] = end_point_x[0] + 10
    end_point_y[1] = end_point_y[1] - 10
    end_point_z[1] = end_point_z[1] + 10
    end_point_z[0] = end_point_z[0] - 10

    cv2.putText(img, 'x', end_point_x, cv2.FONT_HERSHEY_PLAIN,
     0.8, RED, 1, cv2.LINE_AA)
    cv2.putText(img, 'y', end_point_y, cv2.FONT_HERSHEY_PLAIN,
     0.8, GREEN, 1, cv2.LINE_AA)
    cv2.putText(img, 'z', end_point_z, cv2.FONT_HERSHEY_PLAIN,
     0.8, BLUE, 1, cv2.LINE_AA)

MARKER_SIZE = 95 # milimeters
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

# Read intrinsic parameters of the camera
with np.load('bin/camera_matrix.npz') as X:
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
obj_points[1, 0], obj_points[1, 1], obj_points[2, 0] = -MARKER_SIZE/2, -MARKER_SIZE/2, MARKER_SIZE/2
obj_points[2, 1], obj_points[3, 0], obj_points[3, 1] = -MARKER_SIZE/2, MARKER_SIZE/2, MARKER_SIZE/2
obj_points[4, 0], obj_points[4, 1] = -MARKER_SIZE/2, MARKER_SIZE/2

# 3D axis coordinates to be drawn on the ArUco marker 
axis = np.float32([[45, 0, 0], [0, -45, 0], [0, 0, -45]]).reshape(-1, 3)

estimated_pose = np.identity(n=4, dtype=np.float64) # Estimated pose matrix
desired_pose = np.identity(n=4, dtype=np.float64) # Desired pose matrix

# Lists that will store pose info to plot it afterwards
roll_list, pitch_list, yaw_list = [], [], []
x_list, y_list, z_list = [], [], []
x_e_list, y_e_list, z_e_list = [], [], []
roll_e_list, pitch_e_list, yaw_e_list = [], [], []
time_list = []

# figure1, ax1 = plt.subplots(nrows=2, ncols=1, figsize=(7, 5))
# figure2, ax2 = plt.subplots(nrows=2, ncols=1, figsize=(7, 5))

start_time = time.time()

# Set up the GUI window to display the info
root = 'PBVS - info'
cv2.namedWindow(root)
img_info = np.ones((600, 700, 3), np.uint8)

while True:
	# Read frames of the camera
	ret, frame = cap.read()

	cv2.namedWindow(root)
	img_info = np.ones((600, 700, 3), np.uint8)

	# Convert image to gray scale
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	corners, ids, rejected = aruco.detectMarkers(frame_gray, 
												 ARUCO_DICT,
												 K,
												 dist)
	
	# Verify at least one ArUco marker was detected
	if len(corners) > 0 or ids is not None:
		try:
			desired_pose = np.load('bin/desired_pose.npy')
			desired_realworld_tvec = np.load('bin/desired_realworld_tvec.npy')
			desired_euler_angles = np.load('bin/desired_euler_angles.npy')
		except FileNotFoundError:
			print('[INFO]: FileNotFoundError handled, check if all .npy files were loaded')
			pass

		aruco.drawDetectedMarkers(frame, corners)
		current_time = time.time() - start_time

		# Center point between the 4 corners
		aruco_center = np.asarray((abs(corners[0][0][2][0] + corners[0][0][0][0])//2,
							       abs(corners[0][0][2][1] + corners[0][0][0][1])//2)).astype(int)
		
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
								cv2.FONT_HERSHEY_PLAIN, 0.8, RED, 
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
				continue
		
		GUI.display_info_on_screen(img=frame,
								   tvec=realworld_tvec,
								   euler=estimated_euler_angles,
								   tvec_d=desired_realworld_tvec,
								   euler_d=desired_euler_angles)

		# Store pose, and pose error values to plot them
		x_list.append(realworld_tvec[0])
		y_list.append(realworld_tvec[1])
		z_list.append(realworld_tvec[2])

		roll_list.append(roll)
		pitch_list.append(pitch)
		yaw_list.append(yaw)

		x_e_list.append(realworld_tvec[0] - desired_realworld_tvec[0]) 
		y_e_list.append(realworld_tvec[1] - desired_realworld_tvec[1]) 
		z_e_list.append(realworld_tvec[2] - desired_realworld_tvec[2]) 

		roll_e_list.append(roll - desired_euler_angles[0])
		pitch_e_list.append(pitch - desired_euler_angles[1])
		yaw_e_list.append(yaw - desired_euler_angles[2])

		time_list.append(current_time)

		# GUI.display_pose_graphs(time=time_list,
		# 						current_time=current_time,
		# 						x=x_list,
		# 						y=y_list,
		# 						z=z_list,
		# 						R= roll_list,
		# 						P=pitch_list,
		# 						Y=yaw_list,
		# 						axis=ax1)

		# GUI.display_error_graphs(time=time_list,
		# 						 current_time=current_time,
		# 						 x_e=x_e_list,
		# 						 y_e=y_e_list,
		# 						 z_e=z_e_list,
		# 						 R_e= roll_e_list,
		# 						 P_e=pitch_e_list,
		# 						 Y_e=yaw_e_list,
		# 						 axis=ax2)

		plt.pause(0.001) # To constantly refresh the graph

		GUI.display_translation_info(img=img_info,
								     tvec=realworld_tvec,
								     tvec_d=desired_realworld_tvec)

		GUI.display_rotation_info(img=img_info,
								  euler=estimated_euler_angles,
								  euler_d=desired_euler_angles)

		GUI.display_interpretation(img=img_info,
								   tvec=realworld_tvec,
								   euler=estimated_euler_angles,
								   tvec_d=desired_realworld_tvec,
								   euler_d=desired_euler_angles)
	
	GUI.display_background(img_info)
	cv2.imshow(root, img_info)
	cv2.imshow('PVBS - RGB', frame)

	# If 'q' pressed, save the current pose of the ArUco marker 
	if cv2.waitKey(1) & 0xFF == ord('q'):
		desired_pose = estimated_pose
		desired_euler_angles = estimated_euler_angles
		desired_realworld_tvec = realworld_tvec

		np.save('bin/desired_pose.npy', desired_pose)
		np.save('bin/desired_euler_angles.npy', desired_euler_angles)
		np.save('bin/desired_realworld_tvec.npy', desired_realworld_tvec)

		print('[INFO]: ArUco marker pose saved')

	# If ESC pressed exit
	if cv2.waitKey(1) & 0xFF == 27:
		break

# Close all 
cap.release()
cv2.destroyAllWindows()