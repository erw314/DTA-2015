import numpy as np

# Multiply each coordinate of the trip by scale_factor. Returns a list of coordinates.
# scale_factor: float	
def scale(coordinates, scale_factor):
	return [(scale_factor*coord[0], scale_factor*coord[1]) for coord in coordinates]

# Rotate counterclockwise the coordinates of a trip by a specified angle in radians
# angle: float 
def rotate(coordinates, angle):	
	# Rotate the point (x,y) counterclockwise by theta radians
	def rotate(x, y, theta):
		point = np.matrix([[x], [y]])
		rotation_matrix = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
		rotated_point = rotation_matrix * point
		return (rotated_point.item(0,0), rotated_point.item(1,0))

	return map(lambda coord : rotate(coord[0], coord[1], angle), coordinates)	
		
# Rotates the coordinates of a trip so that the trip ends on the positive x axis. Returns a list of coordinates.
def rotate_x_axis(coordinates):
	last_x, last_y = coordinates[-1][0], coordinates[-1][1]
	# angle to rotate the point (last_x, last_y) counterclockwise so that the point lies on the positive x axis
	angle_to_x_axis = -np.arctan2(last_y, last_x)		
	rotated_coordinates = rotate(coordinates, angle_to_x_axis)
	rotated_coordinates[-1] = (np.sqrt(last_x**2+last_y**2), 0) # avoid floating point imprecision
	return rotated_coordinates

# Rotates and scales the trip so that the trip ends at the point (1,0) if trip doesn't end at origin.
# If trip ends at the origin then the original coordiates are returned.
def normalize(coordinates):
	last_x, last_y = coordinates[-1][0], coordinates[-1][1]	
	# Return original coordinates if trip ends at origin
	if (last_x, last_y) == (0, 0):
		return coordinates
	rotated_coordinates_trip = rotate_x_axis(coordinates)
	return scale(rotated_coordinates_trip, 1.0/np.sqrt(last_x**2+last_y**2))
