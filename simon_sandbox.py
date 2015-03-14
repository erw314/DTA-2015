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

from sklearn.svm import SVC


	
'''
# map(lambda x : x[1], 
f = open('driverData_small.p', 'r')
all_drivers = pickle.load(f)

N = 130
M = 40
labels = []
training_trips = []
test_trips = []

for i in range(N):
    training_trips.append(Trip(0, i, all_drivers[0][i]))
    labels.append(1)

for i in range(N):
    training_trips.append(Trip(1, i, all_drivers[1][i]))
    labels.append(-1)

for i in range(N, N+M):
    test_trips.append(Trip(0, i, all_drivers[0][i]))

for i in range(N, N+M):
    test_trips.append(Trip(1, i, all_drivers[1][i]))


print run_SVM(training_trips, labels, 1, test_trips)
'''

