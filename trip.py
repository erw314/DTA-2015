import math
import matplotlib.pyplot as plt
import numpy as np

class Trip:
	# coordinates - list of tuples of floats, where first is (0,0)
	def __init__(self, driver, coordinates):
		self.driver = driver
		self.total_seconds = len(coordinates) - 1
		self.x_coordinates = [coordinate[0] for coordinate in coordinates]
		self.y_coordinates = [coordinate[1] for coordinate in coordinates]

		# Speed at every point in time, where the i-th entry is the average speed between time i and i+1
		self.speeds = [self.interval_distance(i, i+1) for i in range(self.total_seconds)]
		# Absolute acceleration at every point in time, where the i-th entry is the absolute acceleration between time i and i+2
		self.absolute_accelerations = self.discrete_derivative(self.speeds)


		
		self.rotated_coordinates = None # ensures that trip ends on x axis
		self.radius = math.sqrt(self.x_coordinates[-1]**2 + self.y_coordinates[-1]**2) # distance from last point on trip to origin

	# Takes the discrete derivative of data_list, a list of floats. Requires that data_list has at least two elements.
	def discrete_derivative(self, data_list):
		assert len(data_list) >= 2
		return [data_list[i+1] - data_list[i] for i in range(len(data_list) - 1)]


	def plot(self):
		#plt.figure(figsize=(10, 10))
		plt.plot(self.x_coordinates, self.y_coordinates, 'ro-')
		plt.show()

	# Number of seconds of the trip
	def total_time(self):
		return self.total_seconds

	# divide trip into "segments", ex highway local
	# how much the driver turns

	# Distance travelled in the time interval [start_time, end_time]. At time 0 the driver is at the origin.
	# Requires 0 <= start_time <= end_time <= total_seconds
	# start_time: time in seconds to begin calculating distance
	# end_time: time in seconds to stop calculating distance
	def interval_distance(self, start_time, end_time): 
		total_distance = 0
		for i in range(start_time, end_time):
			total_distance += math.sqrt((self.x_coordinates[i+1]-self.x_coordinates[i])**2 + (self.y_coordinates[i+1]-self.y_coordinates[i])**2)
		return total_distance

	# Total distance travelled in trip.
	def total_distance(self):
		return self.interval_distance(0, self.total_seconds)

	

	# Average speed in the time interval [start_time, end_time]. At time 0 the driver is at the origin.
	# Requires 0 <= start_time < end_time <= total_seconds
	# start_time: time in seconds to begin calculating speed
	# end_time: time in seconds to stop calculating speed 	
	def interval_average_speed(self, start_time, end_time):
		return self.interval_distance(start_time, end_time) / (end_time - start_time)

	# Average speed of the entire trip.
	def total_average_speed(self):
		return self.interval_average_speed(0, self.total_seconds)

	# Absolute value of acceleration in the time interval [start_time, end_time]. At time 0 the driver is at the origin.
	# Requires start_time <= end_time - 2
	# start_time: time in seconds to begin calculating absolute acceleration
	# end_time: time in seconds to stop calculating absolute acceleration
	def interval_absolute_acceleration(self, start_time, end_time):
		return (self.speeds[end_time - 1] - self.speeds[start_time]) / (end_time - start_time)

	# Average acceleration of the entire trip.
	def total_absolute_acceleration(self):
		return self.interval_absolute_acceleration(0, self.total_seconds)

	# Multiply each coordinate of the trip by scale_factor. Returns a list of coordinates.
	# scale_factor: float
	def scale_coordinates(self, scale_factor):
		return [(scale_factor*coord[0], scale_factor*coord[1]) for coord in self.coordinates]


	# Rotate counterclockwise the coordinates of a trip by a specified angle in radians
	# angle: float 
	def rotate_coordinates(self, angle):	

		# Rotate the point (x,y) counterclockwise by theta radians
		def rotate(x, y, theta):
			point = np.matrix([[x], [y]])
			rotation_matrix = [[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]]
			rotated_point = rotation_matrix * point
			return (rotated_point.item(0,0), rotated_point.item(1,0))

		return map(lambda coord : rotate(coord[0], coord[1], angle), self.coordinates)	
			
	# Rotates the coordinates of a trip so that the trip ends on the positive x axis. Returns a list of coordinates.
	def rotate_coordinates_to_positive_x_axis(self):
		last_x, last_y = self.x_coordinates[-1], self.y_coordinates[-1]	
		# angle to rotate the point (last_x, last_y) counterclockwise so that the point lies on the positive x axis
		angle_to_x_axis = -math.atan2(last_y, last_x)		
		rotated_coordinates = self.rotate_coordinates(angle_to_x_axis)
		rotated_coordinates[-1] = (self.radius, 0) # avoid floating point imprecision
		return rotated_coordinates

	'''
	# Rotates and scales the trip so that the trip ends at the point (1,0) if trip doesn't end at origin.
	# If trip ends at the origin then the original coordiates are returned.
	def normalize_trip(self):
		last_x, last_y = self.x_coordinates[-1], self.y_coordinates[-1]	
		# Return original coordinates if trip ends at origin
		if (last_x, last_y) == (0, 0):
			return self.coordinates

		rotated_coordinates_trip = Trip(self.rotate_coordinates_to_positive_x_axis())
		return rotated_coordinates_trip.scale_coordinates(1.0/self.radius)
	'''


#coordinates = [(0,0), (3, 4), (8,16)]
coordinates = [(0,0), (3,4), (4,5), (9, 17)]
trip = Trip(0, coordinates)

print trip.total_time()
print trip.speeds
print trip.absolute_accelerations
print trip.interval_absolute_acceleration(0,3)
print trip.interval_absolute_acceleration(1,3)
print trip.total_absolute_acceleration()


'''
print trip.driver 
print trip.coordinates 
print trip.x_coordinates 
print trip.y_coordinates 
print trip.total_seconds 
print trip.total_time
print trip.interval_distance(1,2)
print trip.total_distance()
print trip.interval_average_speed(1,2)
print trip.total_average_speed()
#print trip.plot()
print trip.rotate_coordinates(math.pi/3)
print trip.scale_coordinates(2)
trip2 = Trip(2, trip.rotate_coordinates_to_positive_x_axis())
print trip2.plot()
'''

#print trip.normalize_trip