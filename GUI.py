import cv2
import numpy as np 
import matplotlib.pyplot as plt

root = 'PBVS - info'
cv2.namedWindow(root)

img = np.ones((600, 400, 3), np.uint8)

cv2.line(img, (0, 150), (600, 150), (255, 255, 255), 3)
cv2.line(img, (0, 320), (600, 320), (255, 255, 255), 3)
cv2.line(img, (200, 0), (200, 320), (255, 255, 255), 3)

def display_translation_info(x, x_d, y, y_d, z, z_d):
	""" Outputs the translation info of the ArUco marker

	Parameters:
		x (float): x position of the translation vector
		x_d (float): Desired x position to reach 
		y (float): y position of the translation vector
		y_d (float): Desired y position to reach 
		z (float): z position of the translation vector
		z_d (float): Desired z position to reach 
	"""		
	error_x = x - x_d
	error_y = y - y_d
	error_z = z - z_d

	current_x_str = 'x: {0:4.0f}'.format(x)	
	current_y_str = 'y: {0:4.0f}'.format(y)	
	current_z_str = 'z: {0:4.0f}'.format(z)

	error_x_str = 'xe: {0:4.0f}'.format(error_x)
	error_y_str = 'ye: {0:4.0f}'.format(error_y)
	error_z_str = 'ze: {0:4.0f}'.format(error_z)

	cv2.putText(img, current_x_str, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 1, cv2.LINE_AA)
	cv2.putText(img, current_y_str, (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 100, 255), 1, cv2.LINE_AA)
	cv2.putText(img, current_z_str, (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 1, cv2.LINE_AA)

	cv2.putText(img, error_x_str, (220, 20), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 1, cv2.LINE_AA)
	cv2.putText(img, error_y_str, (220, 75), cv2.FONT_HERSHEY_PLAIN, 2, (0, 100, 255), 1, cv2.LINE_AA)
	cv2.putText(img, error_z_str, (220, 120), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 1, cv2.LINE_AA)

def display_rotation_info(roll, roll_d, pitch, pitch_d, yaw, yaw_d):
	""" Outputs the translation info of the ArUco marker

	Parameters:
		roll (float): Roll position of the translation vector
		roll_d (float): Desired roll position to reach 
		pitch (float): Pitch position of the translation vector
		pitch_d (float): Desired pitch position to reach 
		yaw (float): Yaw position of the translation vector
		yaw_d (float): Desired yaw position to reach 
	"""		
	error_roll = roll - roll_d
	error_pitch = pitch - pitch_d
	error_yaw = yaw - yaw_d

	current_roll_str = 'R: {0:4.0f} '.format(roll)
	current_pitch_str = 'P: {0:4.0f} '.format(pitch)
	current_yaw_str = 'Y: {0:4.0f} '.format(yaw)

	error_roll_str = 'Re: {0:4.0f}'.format(error_roll)
	error_pitch_str = 'Pe: {0:4.0f}'.format(error_pitch)
	error_yaw_str = 'Ye: {0:4.0f}'.format(error_yaw)

	cv2.putText(img, current_roll_str, (10, 200), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 1, cv2.LINE_AA)
	cv2.putText(img, current_pitch_str, (10, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 100, 255), 1, cv2.LINE_AA)
	cv2.putText(img, current_yaw_str, (10, 300), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 1, cv2.LINE_AA)

	cv2.putText(img, error_roll_str, (220, 200), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 0), 1, cv2.LINE_AA)
	cv2.putText(img, error_pitch_str, (220, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 100, 255), 1, cv2.LINE_AA)
	cv2.putText(img, error_yaw_str, (220, 300), cv2.FONT_HERSHEY_PLAIN, 2, (255, 100, 0), 1, cv2.LINE_AA)


while True:
	cv2.imshow(root, img)
	display_translation_info(0, 0, 0, 0, 0, 0)
	display_rotation_info(0, 0, 0, 0, 0, 0)

	if cv2.waitKey(1) & 0xFF == 27:
		break