import numpy as np
import math

def isRotationMatrix(R):
	""" Checks if a matrix is a valid rotation matrix

		Parameters:
		R (ndarray): Rotation matrix

		Returns:
		n (float): Norm close to 0 (with precision of < 1e-6) 
	"""
	Rt = np.transpose(R)
	should_be_identity = np.dot(Rt, R)
	I = np.identity(n=3, dtype=R.dtype)
	n = np.linalg.norm(I - should_be_identity)
	return n < 1e-6

def rotation_matrix_to_euler_angles(R):
	""" Calculates rotation matrix to euler angles
        The result is the same as MATLAB except the order
		the euler angles ( x and z are swapped)

		Parameters:
		R (ndarray): Rotation matrix

		Returns:
		x, y, z (ndarray) = Euler angles, a.k.a Yaw, Pitch, Roll
	"""

	assert(isRotationMatrix(R))

	sy = math.sqrt(R[0,0] * R[0, 0] +  R[1, 0] * R[1, 0])

	singular = sy < 1e-6

	if  not singular:
	    x = math.atan2(R[2, 1] , R[2, 2])
	    y = math.atan2(-R[2, 0], sy)
	    z = math.atan2(R[1, 0], R[0, 0])
	else:
	    x = math.atan2(-R[1, 2], R[1, 1])
	    y = math.atan2(-R[2, 0], sy)
	    z = 0

	return np.array([x, y, z])