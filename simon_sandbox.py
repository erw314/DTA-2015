import math
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
from trip import Trip

f = open('driverData_small.p', 'r')
all_drivers = pickle.load(f)

#trip = Trip(0, 3, all_drivers[0][8])
#trip.plot()

max_abs = []
average_speeds = []
max_accelerations = []

for i in range(200):
	trip = Trip(0, i, all_drivers[0][i])
	max_abs.append(trip.max_abs_acceleration_after_stop())
	average_speeds.append(trip.total_average_speed())
	max_accelerations.append(trip.max_absolute_acceleration())


plt.scatter(average_speeds, max_abs)
plt.show()
