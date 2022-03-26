import cv2
import cv2.aruco as aruco
import numpy as np
import imutils

MARKER_SIZE = 100 # milimeters
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
FPS = 30

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
cap.set(2, CAMERA_WIDTH)
cap.set(4, CAMERA_HEIGHT)
cap.set(5, FPS)

while True:
	# Read frames of the camera
	ret, img = cap.read()

	# Convert image to gray scale
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	corners, ids, rejected = aruco.detectMarkers(img_gray, 
												 ARUCO_DICT,
												 K,
												 dist)

	# Verify at least one ArUco marker was detected
	if len(corners) > 0 or ids is not None:
		aruco.drawDetectedMarkers(img, corners)

		# Get pose of every single marker
		rvec_list_all, tvec_list_all, obj_points = aruco.estimatePoseSingleMarkers(corners, MARKER_SIZE, K, dist)

		rvec = rvec_list_all[0][0]
		tvec = tvec_list_all[0][0]

		# Draw axis and write ids on all markers
		for marker in range(len(ids)):
			aruco.drawAxis(img, K, dist, rvec, tvec, 100)


	cv2.imshow('Aruco Detection - RGB', img)
	cv2.imshow('Aruco Detection - Gray', img_gray)

	# If ESC pressed exit
	if cv2.waitKey(1) & 0xFF == 27:
		break

# Close all 
cap.release()
cv2.destroyAllWindows()