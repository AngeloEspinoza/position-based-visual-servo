import cv2
import numpy as np 
import matplotlib.pyplot as plt

# Colors
RED = (0, 0, 255)
GREEN = (100, 255, 0)
BLUE = (255, 100, 0)
WHITE = (255, 255, 255)

# Text parameters
LINE_TYPE = cv2.LINE_AA
FONT_TYPE = cv2.FONT_HERSHEY_PLAIN

# Tolerance
MILIMETERS_TOLERANCE = 10 # milimeters
DEGREES_TOLERANCE = 10 # degrees

def display_background(img):
	"""Outputs the background lines for the GUI.

	Parameters
	----------
	img : array-like
		Image to be displayed.

	Returns
	-------
	None
	"""
	# Flip by default shape to discharge in the correct variables
	x, y = img.shape[:2][::-1]

	cv2.line(img, (0, y//4), (x, y//4), WHITE, 3)
	cv2.line(img, (0, y//2+20), (x, y//2+20), WHITE, 3)
	cv2.line(img, (x//3, 0), (x//3, y//2+20), WHITE, 3)
	cv2.line(img, ((x//3)*2, 0), ((x//3)*2, y//2+20), WHITE, 3)

def display_translation_info(img, tvec, tvec_d):
	"""Outputs the translation info of the ArUco marker.

	Parameters
	----------
	img : array-like
		Image to be written on the information.
	tvec : array-like
		Array with the x, y, and z positions.
	tvec_d : array-like
		Array with the desired x, y, and z positions.

	Returns
	-------
	None
	"""
	x = tvec[0]
	y = tvec[1]
	z = tvec[2]

	x_d = tvec_d[0]
	y_d = tvec_d[1]
	z_d = tvec_d[2]

	error_x = x - x_d
	error_y = y - y_d
	error_z = z - z_d

	current_x_str = f'x: {x:.0f} mm'	
	current_y_str = f'y: {y:.0f} mm'	
	current_z_str = f'z: {z:.0f} mm'

	desired_x_str = f'xd: {x_d:.0f} mm'	
	desired_y_str = f'yd: {y_d:.0f} mm'	
	desired_z_str = f'zd: {z_d:.0f} mm'

	error_x_str = f'xe: {error_x:.0f} mm'
	error_y_str = f'ye: {error_y:.0f} mm'
	error_z_str = f'ze: {error_z:.0f} mm'

	cv2.putText(img, current_x_str, (10, 20), FONT_TYPE, 2, GREEN, 1, LINE_TYPE)
	cv2.putText(img, current_y_str, (10, 70), FONT_TYPE, 2, RED, 1, LINE_TYPE)
	cv2.putText(img, current_z_str, (10, 120), FONT_TYPE, 2, BLUE, 1, LINE_TYPE)

	cv2.putText(img, desired_x_str, (250, 20), FONT_TYPE, 2, GREEN, 1, LINE_TYPE)
	cv2.putText(img, desired_y_str, (250, 75), FONT_TYPE, 2, RED, 1, LINE_TYPE)
	cv2.putText(img, desired_z_str, (250, 120), FONT_TYPE, 2, BLUE, 1, LINE_TYPE)

	cv2.putText(img, error_x_str, (490, 20), FONT_TYPE, 2, GREEN, 1, LINE_TYPE)
	cv2.putText(img, error_y_str, (490, 75), FONT_TYPE, 2, RED, 1, LINE_TYPE)
	cv2.putText(img, error_z_str, (490, 120), FONT_TYPE, 2, BLUE, 1, LINE_TYPE)

def display_rotation_info(img, euler, euler_d):
	"""Outputs the translation info of the ArUco marker.

	Parameters
	----------
	img : array-like
		Image to be written on the information.
	euler : array-like:
		Array with the roll, pitch, and yaw orientations. 
	euler_d : array-like
		Array with the desired roll, pitch, and yaw orientations.

	Returns
	-------
	None
	"""	
	roll = euler[0]
	pitch = euler[1]
	yaw = euler[2]

	roll_d = euler_d[0]
	pitch_d = euler_d[1]
	yaw_d = euler_d[2]

	error_roll = roll - roll_d
	error_pitch = pitch - pitch_d
	error_yaw = yaw - yaw_d

	current_roll_str = f'R: {roll:.0f} deg'
	current_pitch_str = f'P: {pitch:.0f} deg'
	current_yaw_str = f'Y: {yaw:.0f} deg'

	desired_roll_str = f'Rd: {roll_d:.0f} deg'
	desired_pitch_str = f'Pd: {pitch_d:.0f} deg'
	desired_yaw_str = f'Yd: {yaw_d:.0f} deg'

	error_roll_str = f'Re: {error_roll:.0f} deg'
	error_pitch_str = f'Pe: {error_pitch:.0f} deg'
	error_yaw_str = f'Ye: {error_yaw:.0f} deg'

	cv2.putText(img, current_roll_str, (10, 200), FONT_TYPE, 2, GREEN, 1, LINE_TYPE)
	cv2.putText(img, current_pitch_str, (10, 250), FONT_TYPE, 2, RED, 1, LINE_TYPE)
	cv2.putText(img, current_yaw_str, (10, 300), FONT_TYPE, 2, BLUE, 1, LINE_TYPE)

	cv2.putText(img, desired_roll_str, (250, 200), FONT_TYPE, 2, GREEN, 1, LINE_TYPE)
	cv2.putText(img, desired_pitch_str, (250, 250), FONT_TYPE, 2, RED, 1, LINE_TYPE)
	cv2.putText(img, desired_yaw_str, (250, 300), FONT_TYPE, 2, BLUE, 1, LINE_TYPE)

	cv2.putText(img, error_roll_str, (490, 200), FONT_TYPE, 2, GREEN, 1, LINE_TYPE)
	cv2.putText(img, error_pitch_str, (490, 250), FONT_TYPE, 2, RED, 1, LINE_TYPE)
	cv2.putText(img, error_yaw_str, (490, 300), FONT_TYPE, 2, BLUE, 1, LINE_TYPE)

def display_interpretation(img, tvec, euler, tvec_d, euler_d):
	"""Outputs a message to the user/robot stating how to move.

	Parameters
	----------
	img : array-like
		Image to be written on the information.
	tvec : array-like
		Array with the x, y, and z positions. 
	euler : array-like
		Array with the roll, pitch, and yaw orientations. 
	tvec_d : array-like
		Array with the desired x, y, and z positions. 
	euler_d : array-like
		Array with the desired roll, pitch, and yaw orientations.

	Returns
	-------
	None
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

	error_roll = roll - roll_d
	error_pitch = pitch - pitch_d
	error_yaw = yaw - yaw_d
	
	if is_success_roll(img, error_roll):
		if is_success_pitch(img, error_pitch):
			if is_success_yaw(img, error_yaw):
				if is_success_x(img, error_x):
					if is_success_y(img, error_y):
						is_success_z(img, error_z)

def is_success_x(img, error):
	"""Displays the success message for the x-axis."""
	message_right = f'Translate {abs(error):.0f}mm to the right'
	message_left = f'Translate {abs(error):.0f}mm to the left'
	message_x_success = 'You\'ve reached the desired position in x!'

	if error >= -MILIMETERS_TOLERANCE and error <= MILIMETERS_TOLERANCE:
		cv2.putText(img, message_x_success, (10, 430), FONT_TYPE, 1, GREEN, 1, LINE_TYPE)
		return True
	elif error > MILIMETERS_TOLERANCE:
		cv2.putText(img, message_left, (10, 430), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)
	elif error < MILIMETERS_TOLERANCE:
		cv2.putText(img, message_right, (10, 430), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)

def is_success_y(img, error):
	"""Displays the success message for the y-axis."""
	message_up = f'Translate {abs(error):.0f}mm up'
	message_down = f'Translate {abs(error):.0f}mm down'
	message_y_success = 'You\'ve reached the desired position in y!'

	if error >= -MILIMETERS_TOLERANCE and error <= MILIMETERS_TOLERANCE:
		cv2.putText(img, message_y_success, (10, 450), FONT_TYPE, 1, GREEN, 1, LINE_TYPE)
		return True
	elif error > MILIMETERS_TOLERANCE:
		cv2.putText(img, message_down, (10, 450), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)
	elif error < MILIMETERS_TOLERANCE:
		cv2.putText(img, message_up, (10, 450), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)

def is_success_z(img, error):
	"""Displays the success message for the z-axis."""
	message_frontwards = f'Translate {abs(error):.0f}mm frontwards'
	message_backwards = f'Translate {abs(error):.0f}mm backwards'
	message_z_success = 'You\'ve reached the desired position in z!'

	if error >= -MILIMETERS_TOLERANCE and error <= MILIMETERS_TOLERANCE:
		cv2.putText(img, message_z_success, (10, 470), FONT_TYPE, 1, GREEN, 1, LINE_TYPE)
		return True
	elif error > MILIMETERS_TOLERANCE:
		cv2.putText(img, message_frontwards, (10, 470), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)
	elif error < MILIMETERS_TOLERANCE:
		cv2.putText(img, message_backwards, (10, 470), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)

def is_success_roll(img, error):
	"""Displays the success message for the roll angle."""	
	message_roll = f'Rotate {error:.0f} deg around y'
	message_roll_success = 'You\'ve reached the desired position in roll!'

	if error >= -DEGREES_TOLERANCE and error <= DEGREES_TOLERANCE:
		cv2.putText(img, message_roll_success, (10, 350), FONT_TYPE, 1, GREEN, 1, LINE_TYPE)
		return True
	elif error > DEGREES_TOLERANCE or error < DEGREES_TOLERANCE:
		cv2.putText(img, message_roll, (10, 350), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)

def is_success_pitch(img, error):
	"""Displays the success message for the pitch angle."""
	message_pitch = f'Rotate {error:.0f} deg around x'
	message_pitch_success = 'You\'ve reached the desired position in pitch!'

	if error >= -DEGREES_TOLERANCE and error <= DEGREES_TOLERANCE:
		cv2.putText(img, message_pitch_success, (10, 370), FONT_TYPE, 1, GREEN, 1, LINE_TYPE)
		return True
	elif error > DEGREES_TOLERANCE or error < DEGREES_TOLERANCE:
			cv2.putText(img, message_pitch, (10, 370), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)
	
def is_success_yaw(img, error):
	"""Displays the success message for the yaw angle."""	
	message_yaw = f'Rotate {error:.0f} deg around z'
	message_yaw_success = 'You\'ve reached the desired position in yaw!'

	if error >= -DEGREES_TOLERANCE and error <= DEGREES_TOLERANCE:
		cv2.putText(img, message_yaw_success, (10, 390), FONT_TYPE, 1, GREEN, 1, LINE_TYPE)
		return True
	elif error > DEGREES_TOLERANCE or error < DEGREES_TOLERANCE:
				cv2.putText(img, message_yaw, (10, 390), FONT_TYPE, 1, WHITE, 1, LINE_TYPE)

def display_info_on_screen(img, tvec, euler, tvec_d, euler_d):
	"""Outputs the pose and desired pose of the ArUco marker on screen.

	Parameters
	----------
	img : array-like
		Image to be written on the information.
	tvec : array-like
		Array with the x, y, and z positions. 
	euler : array-like
		Array with the roll, pitch, and yaw orientations. 
	tvec_d : array-like
		Array with the desired x, y, and z positions. 
	euler_d : array-like
		Array with the desired roll, pitch, and yaw orientations. 

	Returns
	-------
	None
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

	desired_realworld_tvec_x_str = f'Desired x: {x_d:.0f} mm'
	desired_realworld_tvec_y_str = f'Desired y: {y_d:.0f} mm'
	desired_realworld_tvec_z_str = f'Desired z: {z_d:.0f} mm'
						
	error_x_str = f'Error x: {x - x_d:.0f} mm'
	error_y_str = f'Error y: {y - y_d:.0f} mm'
	error_z_str = f'Error z: {z - z_d:.0f} mm'

	desired_euler_angles_roll_str = f'Desired roll: {roll_d:.0f} deg'
	desired_euler_angles_pitchstr = f'Desired pitch: {pitch_d:.0f} deg'
	desired_euler_angles_yaw_str = f'Desired yaw: {yaw_d:.0f} deg'

	error_roll_str = f'Error roll: {roll - roll_d:.0f} deg'
	error_pitch_str = f'Error pitch: {pitch - pitch_d:.0f} deg'
	error_yaw_str = f'Error yaw: {yaw - yaw_d:.0f} deg'

	current_x_str = f'x = {x:.0f} mm'
	current_y_str = f'y = {y:.0f} mm'
	current_z_str = f'z = {z:.0f} mm'

	current_pitch_str = f'pitch = {pitch:.0f} deg'
	current_roll_str = f'roll = {roll:.0f} deg'
	current_yaw_str = f'yaw = {yaw:.0f} deg'

	cv2.putText(img, desired_realworld_tvec_x_str, (450, 10), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, desired_realworld_tvec_y_str, (450, 20), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, desired_realworld_tvec_z_str, (450, 30), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	
	cv2.putText(img, error_x_str, (450, 50), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, error_y_str, (450, 60), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, error_z_str, (450, 70), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)

	cv2.putText(img, desired_euler_angles_roll_str, (450, 90), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, desired_euler_angles_pitchstr, (450, 100), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, desired_euler_angles_yaw_str, (450, 110), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	
	cv2.putText(img, error_roll_str, (450, 130), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, error_pitch_str, (450, 140), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, error_yaw_str, (450, 150), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)

	cv2.putText(img, current_x_str, (5, 10), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, current_y_str, (5, 20), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, current_z_str, (5, 30), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)

	cv2.putText(img, current_roll_str, (5, 50), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, current_pitch_str, (5, 60), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)
	cv2.putText(img, current_yaw_str, (5, 70), FONT_TYPE, 0.8, RED, 1, LINE_TYPE)

def display_pose_graphs(time, current_time, x, y, z, R, P, Y, axis):
	"""Draws the pose graphs of the ArUco marker.

	Parameters
	----------
	time : list
		List containing the time elapsed. 
	x : list
		List containing the x positions stored of the ArUco marker.
	y : list
		List containing the y positions stored of the ArUco marker.
	z : list
		List containing the z positions stored of the ArUco marker.
	R : list
		List containing the roll orientation stored of the ArUco marker.
	P : list
		List containing the pitch orientation stored of the ArUco marker.
	Y : list
		List containing the yaw orientation stored of the ArUco marker.
	axis : array-like
		Axis to be displayed on.

	Returns
	-------
	None
	"""
	axis[0].plot(time, x, color='b', label='x')
	axis[0].plot(time, y, color='g', label='y')
	axis[0].plot(time, z, color='r', label='z')

	axis[1].plot(time, R, color='g', label='R')
	axis[1].plot(time, P, color='r', label='P')
	axis[1].plot(time, Y, color='b', label='Y')

	axis[0].set_xlim(left=max(0, current_time-10), right=current_time+10)
	axis[1].set_xlim(left=max(0, current_time-10), right=current_time+10)

	if len(x) == 1:
		axis[0].legend(loc='upper right')
		axis[0].set_ylabel('Camera \nposition (mm)')

		axis[1].legend(loc='upper right')
		axis[1].set_xlabel('Time (s)')
		axis[1].set_ylabel('Camera \norientation (deg)')

def display_error_graphs(time, current_time, x_e, y_e, z_e, R_e, P_e, Y_e, axis):
	"""Draws the pose graphs of the ArUco marker.

	Parameters
	----------
	time : list
		List containing the time elapsed. 
	x_e : list
		List containing the x position error recorded of the ArUco marker.
	y_e : list
		List containing the y position error recorded of the ArUco marker.
	z_e : list
		List containing the z position error recorded of the ArUco marker.
	R_e : list
		List containing the roll angle recorded of the ArUco marker.
	P_e : list
		List containing the pitch angle recorded of the ArUco marker.
	Y_e : list
		List containing the yaw angle recorded of the ArUco marker.
	axis : array-like
		Axis to be displayed on.

	Returns
	-------
	None
	"""
	axis[0].plot(time, x_e, color='g', label='Error x')
	axis[0].plot(time, y_e, color='r', label='Error y')
	axis[0].plot(time, z_e, color='b', label='Error z')

	axis[1].plot(time, R_e, color='g', label='Error R')
	axis[1].plot(time, P_e, color='r', label='Error P')
	axis[1].plot(time, Y_e, color='b', label='Error Y')

	axis[0].set_xlim(left=max(0, current_time-10), right=current_time+10)
	axis[1].set_xlim(left=max(0, current_time-10), right=current_time+10)

	if len(x_e) == 1:
		axis[0].legend(loc='upper right')
		axis[0].set_ylabel('Camera \nposition error (mm)')

		axis[1].legend(loc='upper right')
		axis[1].set_xlabel('Time (s)')
		axis[1].set_ylabel('Camera \norientation error (deg)')