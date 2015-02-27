import math
import matplotlib.pyplot as plt
import numpy as np

# figure out speeds vs velocities vs abs acclerations

class Trip:
	# coordinates - list of tuples of floats, where first is (0,0)
	def __init__(self, driver, coordinates):
		self.driver = driver # driver ID
		self.total_seconds = len(coordinates) - 1
		self.x_coordinates = [float(coordinate[0]) for coordinate in coordinates]
		self.y_coordinates = [float(coordinate[1]) for coordinate in coordinates]

		# Length of the vector (x,y) using Euclidean distance
		def norm((x, y)):
			return math.sqrt(x**2 + y**2)

		self.coordinates = zip(self.x_coordinates, self.y_coordinates) # ensure that entries are pairs of floats
		self.velocities = self.discrete_vector_derivative(self.coordinates)
		# Speed at every point in time, where the i-th entry is the average speed between time i and i+1
		self.speeds = map(norm, self.velocities)
		self.accelerations = self.discrete_vector_derivative(self.velocities)		
		# Absolute acceleration at every point in time, where the i-th entry is the absolute acceleration between time i and i+2
		self.absolute_accelerations = map(norm, self.accelerations)

	# Length of the vector (x,y) using Euclidean distance
	def norm(self, (x, y)):
		return math.sqrt(x**2 + y**2)

	# Takes the discrete derivative of data_list, a list of floats. Requires that data_list has at least two elements.
	def discrete_derivative(self, data_list):
		assert len(data_list) >= 2
		return [data_list[i+1] - data_list[i] for i in range(len(data_list) - 1)]

	# Takes the discrete derivative of vector_list, a list of tuples (x, y). Requires that vector_list has at least two elements.
	def discrete_vector_derivative(self, vector_list):
		assert len(vector_list) >= 2
		x_coordinates = [vector[0] for vector in vector_list]
		y_coordinates = [vector[1] for vector in vector_list]
		return zip(self.discrete_derivative(x_coordinates), self.discrete_derivative(y_coordinates))

	def plot(self):
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

	# Returns each velocity in the time interval [start_time, end_time]
	def interval_velocities(self, start_time, end_time):
		return self.velocities[start_time:end_time + 1]


	# Average speed in the time interval [start_time, end_time]. At time 0 the driver is at the origin.
	# Requires 0 <= start_time < end_time <= total_seconds
	# start_time: time in seconds to begin calculating speed
	# end_time: time in seconds to stop calculating speed 	
	def interval_average_speed(self, start_time, end_time):
		return self.interval_distance(start_time, end_time) / (end_time - start_time)

	# Average speed of the entire trip.
	def total_average_speed(self):
		return self.interval_average_speed(0, self.total_seconds)

	# Max speed over the entire trip
	def max_speed(self):
		return max(self.speeds)

	# Returns each acceleration in the time interval [start_time, end_time]
	def interval_accelerations(self, start_time, end_time):
		return self.accelerations[start_time:end_time + 1]


	# Average acceleration in the time interval [start_time, end_time]. At time 0 the driver is at the origin.
	# Requires start_time <= end_time - 2 
	def interval_acceleration(self, start_time, end_time):
		t = end_time - start_time - 1
		return ((self.velocities[end_time-1][0] - self.velocities[start_time][0]) / t, (self.velocities[end_time-1][1] - self.velocities[start_time][1]) / t)

	def interval_absolute_acceleration(self, start_time, end_time):
		return self.norm(self.interval_acceleration(start_time, end_time))

	# Average absolute acceleration of the entire trip.
	def total_absolute_acceleration(self):
		return self.interval_absolute_acceleration(0, self.total_seconds)

	# Max absolute acceleration over the entire trip
	def max_absolute_acceleration(self):
		return max(self.absolute_accelerations)

	# Maximum acceleration after all stoppages (defined as having a speed of less than 1)
	def max_abs_acceleration_after_stop(self):
		stop_speed_cutoff = 1 # if the speed is less than this value then the car has stopped
		accelerations_after_stop = []
		for i in range(len(self.absolute_accelerations)):
			if self.speeds[i] < stop_speed_cutoff:
				accelerations_after_stop.append(self.absolute_accelerations[i])

		# No stoppages found
		if len(accelerations_after_stop) == 0:
			return 0

		return max(accelerations_after_stop)



#coordinates = [(0,0), (3, 4), (8,16)]
coordinates = [(0,0), (3,4), (3,3.5), (9, 17), (-1, -3), (2, 2), (1.7, 1.8), (1, 2)]
trip = Trip(0, coordinates)

#print trip.velocities
#print trip.speeds
#print trip.max_speed()
#print trip.max_abs_acceleration_after_stop()

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