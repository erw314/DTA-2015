import math
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle
from trip import Trip

# trips - Data set of n Trip objects
# returns list of n d-dimensional feature vectors, represented as numpy arrays
def extract_feature_vectors(trips):
	d = 5 # number of features
	feature_vectors = []
	for trip in trips:
		feature_vector = np.zeros(d)
		feature_vector[0] = trip.max_speed()
		feature_vector[1] = trip.total_average_speed()
		feature_vector[2] = trip.max_absolute_acceleration()
		feature_vector[3] = trip.total_absolute_acceleration()
		feature_vector[4] = trip.max_abs_acceleration_after_stop()

		feature_vectors.append(feature_vector)

	return feature_vectors

# normalize feature vectors for SVM

