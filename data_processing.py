import math
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
import cPickle as pickle
from trip import Trip
import os
from sklearn.svm import SVC


def extract_feature_vectors(trips):
    '''
    input list of n Trip objects
    returns list of n d-dimensional feature vectors
    '''
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


def extract_normalized_feature_vectors(trips):
    '''
    input list of n Trip objects
    returns n by d numpy array with d normalized features for radial basis SVM
    normalized with mean 0, s.d. 1
    '''
    return preprocessing.scale(extract_feature_vectors(trips))
    
def run_SVM(training_trips, labels, c, test_trips):
    '''
    training_trips - list of n Trip objects
    labels - n labels corresponding to the trips
    test_trips - list of m Trip objects
    Returns list of m probabilities using an SVM with the radial basis function kernel, 
    where the i-th probability is the certainty of the i-th test trip to have a positive label
    '''
    # Convert training and test data to normalized feature vectors
    normalized_training_feature_vectors = extract_normalized_feature_vectors(training_trips)
    normalized_test_feature_vectors = extract_normalized_feature_vectors(test_trips)

    # Train SVM
    svm = SVC(C=c, kernel = 'rbf', probability = True)
    svm.fit(normalized_training_feature_vectors, labels)

    return map(lambda x : x[1], svm.predict_proba(normalized_test_feature_vectors)) 

    #svm.predict(normalized_test_feature_vectors), svm.score(normalized_training_feature_vectors, labels)

def get_false_trips(samples, not_driver):
    '''
    input number of samples, and driver to not choose from
    returns list of randomly chosen Trip objects
    '''
    all_false = []
    files = []
    for n in os.listdir('./'):
        if n[:11] == 'driverData_' and n[11:] != str(int(not_driver)/57)+'.p' and n[11:] != 'small.p': 
            files.append(n)
    print files
    data_file = np.random.choice(files)
    
    with open(data_file, 'r') as f:
        temp_drivers = pickle.load(f)
    
    try:
        i = int(data_file[:-2][11:])

        trips = zip(np.random.choice(range(len(temp_drivers)), samples, replace=False), np.random.choice(range(200), samples, replace=False))

        for t in trips:
            all_false.append(Trip(57*i+t[0], t[1], temp_drivers[t[0]][t[1]]))
    except:
        del temp_drivers
        raise
        
    return all_false
    
 
def label_trips(true_matrix, false_matrix):
    '''
    input correct matrix, and incorrect matrix
    returns two lists of labels for the matrices
    '''
    true_labels = [1 for i in range(len(true_matrix))]
    false_labels = [-1 for i in range(len(false_matrix))]
    return true_labels, false_labels
    
    
def distance(trip1, trip2):
    '''
    input two trip objects
    returns distance between trips, either itself or reflected (Mahalanobis distance)
    '''
    path1, path2 = trip1.coordinates, trip2.coordinates
    if len(path1) > len(path2):
        for i in range(len(path1)-len(path2)):
            path2.append(path2[-1])
    if len(path1) < len(path2):
        for i in range(len(path2)-len(path1)):
            path1.append(path1[-1])
    distance = sum([((path1[i][0]-path2[i][0])**2+(path1[i][1]-path2[i][1])**2)**0.5 for i in range(len(path1))])
    path1 = tf.reflect(path1)
    distanceR = sum([((path1[i][0]-path2[i][0])**2+(path1[i][1]-path2[i][1])**2)**0.5 for i in range(len(path1))])
    return min(distance,distanceR)


