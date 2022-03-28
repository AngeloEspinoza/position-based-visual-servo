import cv2
import cv2.aruco as aruco
import numpy as np
import imutils

MARKER_SIZE = 100 # milimeters
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

		# Draw axis and corners of the markers
		for marker in range(len(ids)):
			for corner in range(4):
				corner_x, corner_y = corners[marker][0, corner]
				center_coordinates = tuple((int(corner_x), int(corner_y)))
				cv2.circle(frame, center_coordinates, 5, BLUE, -1)

			aruco.drawAxis(frame, K, dist, rvec_list_all[marker], tvec_list_all[marker], 50)

		tvec_str_x = 'x = {0:4.0f}'.format(tvec[0])
		tvec_str_y = 'y = {0:4.0f}'.format(tvec[1])
		tvec_str_z = 'z = {0:4.0f}'.format(tvec[2])
		cv2.putText(frame, tvec_str_x, (50, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_str_y, (50, 65), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
		cv2.putText(frame, tvec_str_z, (50, 80), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)


	cv2.imshow('Aruco Detection - RGB', frame)
	cv2.imshow('Aruco Detection - Gray', frame_gray)


	# If ESC pressed exit
	if cv2.waitKey(1) & 0xFF == 27:
		break

# Close all 
cap.release()
cv2.destroyAllWindows()