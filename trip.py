import math
import matplotlib.pyplot as plt

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

	# Rotate coordinates of a trip so that the first 
	def rotate_coordinates(self, coordinates, angle):		
		return None


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
print trip.plot()
