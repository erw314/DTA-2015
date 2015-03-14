import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
import cPickle as pickle
from trip import Trip

# trips - Data set of n Trip objects
# Returns list of n d-dimensional feature vectors, each represented as a list
def extract_feature_vectors(trips):
	d = 5 # number of features
	feature_vectors = []
	for trip in trips:
		feature_vector = [0 for i in range(d)]
		feature_vector[0] = trip.max_speed()
		feature_vector[1] = trip.total_average_speed()
		feature_vector[2] = trip.max_absolute_acceleration()
		feature_vector[3] = trip.total_absolute_acceleration()
		feature_vector[4] = trip.max_abs_acceleration_after_stop()

		feature_vectors.append(feature_vector)

	return feature_vectors




# trips - Data set of n Trip objects
# Returns n x d numpy array where there are d features and we have normalized 
# the feature vectors for a radial basis function SVM such that the values 
# for each feature have mean 0 and standard deviation 1
def extract_normalized_feature_vectors(trips):
	return preprocessing.scale(extract_feature_vectors(trips))
