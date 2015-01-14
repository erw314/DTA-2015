import math
import matplotlib.pyplot as plt
import numpy as np

class Trip:
	# coordinates - list of tuples of floats, where first is (0,0)
	def __init__(self, driver, coordinates):
		self.driver = driver
		self.coordinates = coordinates
		self.x_coordinates = [coordinate[0] for coordinate in coordinates]
		self.y_coordinates = [coordinate[1] for coordinate in coordinates]
		self.total_seconds = len(coordinates) - 1
		self.rotated_coordinates = None # ensures that trip ends on x axis

	def plot(self):
		plt.plot(self.x_coordinates, self.y_coordinates, 'ro-')
		plt.show()

	def interval_distance(self, start_time, end_time): 
		total_distance = 0
		for i in range(start_time, end_time):
			total_distance += math.sqrt((self.x_coordinates[i+1]-self.x_coordinates[i])**2 + (self.y_coordinates[i+1]-self.y_coordinates[i])**2)
		return total_distance

	def total_distance(self):
		return self.interval_distance(0, self.total_seconds)

	# start_time: time in seconds to start calculating speed  	
	def interval_average_speed(self, start_time, end_time):
		return self.interval_distance(start_time, end_time) / (end_time - start_time)

	def total_average_speed(self):
		return self.interval_average_speed(0, self.total_seconds)

	def interval_absolute_acceleration(self):
		return None

	def total_absolute_acceleration(self):
		return None

	def scale_coordinates(self, scale_factor):
		return [(scale_factor*coord[0], scale_factor*coord[1]) for coord in coordinates]


	# Rotate counterclockwise the coordinates of a trip by a specified angle in radians
	def rotate_coordinates(self, angle):	

		# Rotate the point (x,y) counterclockwise by theta radians
		def rotate(x, y, theta):
			point = np.matrix([[x], [y]])
			rotation_matrix = [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]
			rotated_point = rotation_matrix * point
			return (rotated_point.item(0,0), rotated_point.item(1,0))

		return map(lambda coord : rotate(coord[0], coord[1], angle), self.coordinates)	
			




'''
		last_x, last_y = self.x_coordinates[-1], self.y_coordinates[-1]	
		# angle to rotate the point (last_x, last_y) counterclockwise so that the point lies on the positive x axis
		angle_to_x_axis = -math.atan2(last_y, last_x)
'''

coordinates = [(0,0), (3,4), (4,5)]
trip = Trip(0, coordinates)
print trip.driver 
print trip.coordinates 
print trip.x_coordinates 
print trip.y_coordinates 
print trip.total_seconds 
print trip.interval_distance(1,2)
print trip.total_distance()
print trip.interval_average_speed(1,2)
print trip.total_average_speed()
#print trip.plot()
print trip.rotate_coordinates(math.pi/3)
print trip.scale_coordinates(2)