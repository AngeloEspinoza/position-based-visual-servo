import cv2
import cv2.aruco as aruco
import numpy as np
import imutils
import rotm2euler
import math
import os
import matplotlib.pyplot as plt
import time

MARKER_SIZE = 95 # milimeters
BLUE = (255, 0, 0)

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

# Desired pose of the goal with respect to camera
x_desired = 8
y_desired = -274
z_desired = 146
roll_desired = 1
pitch_desired = -111
yaw_desired = 5

C_Te_G = np.identity(n=4, dtype=np.float64) # Estimated pose matrix
Cd_T_G = np.identity(n=4, dtype=np.float64) # Desired pose matrix

roll_list, pitch_list, yaw_list = [], [], []
x, y, z = [], [], []
time_list = []
figure, axis = plt.subplots(nrows=2, ncols=1, figsize=(7, 3))

start_time = time.time()

while True:
	# Read frames of the camera
	ret, frame = cap.read()

	# Convert image to gray scale
	frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	corners, ids, rejected = aruco.detectMarkers(frame_gray, 
												 ARUCO_DICT,
												 K,
												 dist)

	cv2.circle(frame, (287, 231), 5, BLUE, -1)

	# Verify at least one ArUco marker was detected
	if len(corners) > 0 or ids is not None:
		aruco.drawDetectedMarkers(frame, corners)

		# Get pose of every single marker
		rvec_list_all, tvec_list_all, obj_points = aruco.estimatePoseSingleMarkers(corners, MARKER_SIZE, K, dist)

		rvec = rvec_list_all[0][0]
		tvec = tvec_list_all[0][0]

		Cd_T_G = np.load('Cd_T_G.npy')

		current_time = time.time() - start_time

		# Draw axis and corners of the markers
		for marker in range(len(ids)):
			for corner in range(4):
				corner_x, corner_y = corners[marker][0, corner]
				center_coordinates = tuple((int(corner_x), int(corner_y)))
				cv2.circle(frame, center_coordinates, 5, BLUE, -1)

			aruco.drawAxis(frame, K, dist, rvec_list_all[marker], tvec_list_all[marker], 45)

			# Going up increases y-axis, going left increases x-axis,
			# going backwards increases z-axis. In the same way but
			# for the opposite movementes of every axis.
			# Tentative to just change the z-axis by multiplying it by -1
			rvec_flipped = rvec * -1
			tvec_flipped = tvec * -1

			# Convert rvec to a rotation matrix
			R, jacobian = cv2.Rodrigues(rvec_flipped)
			realworld_tvec = np.dot(R, tvec_flipped)
			# print(R, tvec_flipped)

			pitch, roll, yaw =  rotm2euler.rotation_matrix_to_euler_angles(R)

			# Construct homogeneous transformation matrix
			C_Te_G[:3, :3] = R
			C_Te_G[:3, 3] = realworld_tvec

			# print('----------')
			# print('C_Te_G = {}'.format(C_Te_G))
			# print('----------')
			
			# Required motion
			T_delta = C_Te_G @ np.linalg.inv(Cd_T_G)

		tvec_str_x = 'x = {0:4.0f}'.format(tvec_flipped[0])
		tvec_str_y = 'y = {0:4.0f}'.format(tvec_flipped[1])
		tvec_str_z = 'z = {0:4.0f}'.format(tvec_flipped[2])

		rvec_str_pitch = 'pitch = {0:4.0f}'.format(math.degrees(pitch))
		rvec_str_roll = 'roll = {0:4.0f}'.format(math.degrees(roll))
		rvec_str_yaw = 'yaw = {0:4.0f}'.format(math.degrees(yaw))

		cv2.putText(frame, tvec_str_x, (5, 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_str_y, (5, 20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_str_z, (5, 30), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

		cv2.putText(frame, rvec_str_roll, (5, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, rvec_str_pitch, (5, 60), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, rvec_str_yaw, (5, 70), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

		# # Clear terminal
		# os.system('cls')

		print(rvec_list_all)

		x.append(realworld_tvec[0])
		y.append(realworld_tvec[1])
		z.append(realworld_tvec[2])

		roll_list.append(math.degrees(roll))
		pitch_list.append(math.degrees(pitch))
		yaw_list.append(math.degrees(yaw))

		time_list.append(current_time)

		axis[0].plot(time_list, x, color='b', label='x')
		axis[0].plot(time_list, y, color='g', label='y')
		axis[0].plot(time_list, z, color='r', label='z')

		axis[1].plot(time_list, roll_list, color='g', label='roll')
		axis[1].plot(time_list, pitch_list, color='r', label='pitch')
		axis[1].plot(time_list, yaw_list, color='b', label='yaw')

		if len(x) == 1:  
			axis[0].legend(loc='upper right')
			axis[1].legend(loc='upper right')

		plt.pause(0.001)
		
	cv2.imshow('Aruco Detection - RGB', frame)
	# cv2.imshow('Aruco Detection - Gray', frame_gray)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		Cd_T_G = C_Te_G
		np.save('Cd_T_G.npy', Cd_T_G)
	# If ESC pressed exit
	if cv2.waitKey(1) & 0xFF == 27:
		break

# Close all 
cap.release()
cv2.destroyAllWindows()