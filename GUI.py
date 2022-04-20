import cv2
import numpy as np 
import matplotlib.pyplot as plt

def display_background(img):
	""" Outputs the background lines for the GUI

		Parameters:
			img (ndarray): Image to be displayed
	"""
	cv2.line(img, (0, 150), (600, 150), (255, 255, 255), 3)
	cv2.line(img, (0, 320), (600, 320), (255, 255, 255), 3)
	cv2.line(img, (200, 0), (200, 320), (255, 255, 255), 3)


def display_translation_info(img, tvec, euler, tvec_d, euler_d):
	""" Outputs the translation info of the ArUco marker

		Parameters:
			img (ndarray): Image to be written on the information
	"""
	x = tvec[0]
	y = tvec[1]
	z = tvec[2]

	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]

	x_d = tvec_d[0]
	y_d = tvec_d[1]
	z_d = tvec_d[2]

	roll_d = euler_d[0]
	pitch_d = euler_d[1]
	yaw_d = euler_d[2]

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

def display_rotation_info(img, tvec, euler, tvec_d, euler_d):
	""" Outputs the translation info of the ArUco marker

		Parameters:
			img (ndarray): Image to be written on the information
	"""	
	x = tvec[0]
	y = tvec[1]
	z = tvec[2]

	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]

	x_d = tvec_d[0]
	y_d = tvec_d[1]
	z_d = tvec_d[2]

	roll_d = euler_d[0]
	pitch_d = euler_d[1]
	yaw_d = euler_d[2]

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

def display_info_on_screen(img, tvec, euler, tvec_d, euler_d):
	""" Outputs the pose and desired pose of the ArUco marker on screen
		Parameters:
			img (ndarray): Image to be written on the information
			tvec (ndarray): Array with the x, y, and z translations 
			euler (ndarray): Array with the roll, pitch, and yaw rotations 
			tvec_d (ndarray): Array with the desired x, y, and z translations 
			euler_d (ndarray): Array with the desired roll, pitch, and yaw rotations 
	"""
	x = tvec[0]
	y = tvec[1]
	z = tvec[2]

	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]

	x_d = tvec_d[0]
	y_d = tvec_d[1]
	z_d = tvec_d[2]

	roll_d = euler_d[0]
	pitch_d = euler_d[1]
	yaw_d = euler_d[2]

	desired_realworld_tvec_x_str = 'Desired x: {0:4.0f} mm'.format(x_d)
	desired_realworld_tvec_y_str = 'Desired y: {0:4.0f} mm'.format(y_d)
	desired_realworld_tvec_z_str = 'Desired z: {0:4.0f} mm'.format(z_d)
						
	error_x_str ='Error x: {0:4.0f} mm'.format(x - x_d)
	error_y_str ='Error y: {0:4.0f} mm'.format(y - y_d)
	error_z_str ='Error z: {0:4.0f} mm'.format(z - z_d)

	desired_euler_angles_roll_str = 'Desired roll: {0:4.0f} deg'.format(roll_d)
	desired_euler_angles_pitchstr = 'Desired pitch: {0:4.0f} deg'.format(pitch_d)
	desired_euler_angles_yaw_str = 'Desired yaw: {0:4.0f} deg'.format(yaw_d)

	error_roll_str ='Error roll: {0:4.0f} deg'.format(roll - roll_d)
	error_pitch_str ='Error pitch: {0:4.0f} deg'.format(pitch - pitch_d)
	error_yaw_str ='Error yaw: {0:4.0f} deg'.format(yaw - yaw_d)

	current_x_str = 'x = {0:4.0f} mm'.format(x)
	current_y_str = 'y = {0:4.0f} mm'.format(y)
	current_z_str = 'z = {0:4.0f} mm'.format(z)

	current_pitch_str = 'pitch = {0:4.0f} deg'.format(pitch)
	current_roll_str = 'roll = {0:4.0f} deg'.format(roll)
	current_yaw_str = 'yaw = {0:4.0f} deg'.format(yaw)

	cv2.putText(img, desired_realworld_tvec_x_str, (450, 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, desired_realworld_tvec_y_str, (450, 20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, desired_realworld_tvec_z_str, (450, 30), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	
	cv2.putText(img, error_x_str, (450, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, error_y_str, (450, 60), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, error_z_str, (450, 70), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

	cv2.putText(img, desired_euler_angles_roll_str, (450, 90), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, desired_euler_angles_pitchstr, (450, 100), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, desired_euler_angles_yaw_str, (450, 110), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	
	cv2.putText(img, error_roll_str, (450, 130), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, error_pitch_str, (450, 140), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, error_yaw_str, (450, 150), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

	cv2.putText(img, current_x_str, (5, 10), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, current_y_str, (5, 20), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, current_z_str, (5, 30), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

	cv2.putText(img, current_roll_str, (5, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, current_pitch_str, (5, 60), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
	cv2.putText(img, current_yaw_str, (5, 70), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1, cv2.LINE_AA)