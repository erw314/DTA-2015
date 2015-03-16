
## importing libraries, files, etc.
import numpy as np
import matplotlib.pyplot as plt
import cPickle as pickle
import csv
import os

from trip import Trip
import transform as tf
import data_processing as dp


## creating trip objects for analysis

# Constants to be used throughout.
trips_per_driver = 200
drivers_per_pickle = 48
num_pickle = 57

def predict(driver_original_index):

    num_false_samples = 100

    ## creating trip objects for analysis ###############################

    # Choose driver index for classification.
    driver_index = driver_original_index - 1
    driver_index = driver_index % drivers_per_pickle
    drivers_file = 'driverData_'+str(int(driver_index)/drivers_per_pickle)+'.p'
    
    with open(drivers_file, 'r') as f:
        drivers = pickle.load(f)
    driver = drivers[driver_index]
    
    false_trips = []
    random_trips = zip(np.random.choice([i for i in range(len(drivers)) if i!=driver_index], num_false_samples), np.random.choice(range(200), num_false_samples, replace=False))
    for t in random_trips:
        false_trips.append(Trip(driver_original_index-driver_index+t[0], t[1], drivers[t[0]][t[1]]))
    
    del drivers

    trips = [Trip(driver_index, i, driver[i]) for i in range(trips_per_driver)]
    

    ## spacial similarity ###############################################

    # Transform all the trips by rotating to x-axis.
    trips_rotated = [Trip(driver_index, i, tf.rotate_x_axis(trips[i].coordinates)) for i in range(trips_per_driver)]

    # Comparison algorithm to get sets of similar trips.
    def set_compare(stuff, threshold):
        sets_dict = {}
        no_matches = set(stuff)

        for a in stuff:
            if a in no_matches:
                search_from = no_matches | set(sets_dict.keys())
                for b in search_from:
                    if a != b and abs(len(a.coordinates)-len(b.coordinates))/float(len(a.coordinates)) < 0.2: # cannot differ too much
                        if (dp.distance(a, b) <= threshold and max([x[0] for x in a.coordinates]) > 1000
                            and max([x[0] for x in b.coordinates]) > 1000):
                                sets_dict.setdefault(a, set([a])).add(b)
                                no_matches.discard(a)
                                no_matches.discard(b)
        
        return sets_dict, no_matches

    # Optional: select sets of certain size.
    def set_select(sets, threshold):
        new_sets = []
        
        if threshold < 1 and threshold > 0:
            new_sets = sorted([len(s) for s in sets])[:len(sets)*threshold]
            
        elif threshold > 1:
            for s in sets:
                if len(s) > threshold:
                    new_sets.append(s)
        
        return new_sets

    # Find distances between all trips and takes those that have at least one match.
    threshold_distance = 100
    true_sets = set_compare(trips_rotated, threshold_distance)[0]
    while len(true_sets) < 10:
        threshold_distance += 100
        true_sets = set_compare(trips_rotated, threshold_distance)[0]
    
    true_trips = list(set().union(*true_sets.values()))

    # Optional: plot trips in each set for visual verification.
    # for s in true_sets:
        # if len(true_sets[s]) == 2:
            # for x in true_sets[s]:
                # plt.plot(x.x_coordinates, x.y_coordinates)
            # plt.show()


    ## create training sets ##############################################

    # Selecting false trips. Be careful, get_false_trips opens a large file and may slow down performance.
    # false_trips = dp.get_false_trips(len(true_trips), driver_index)

    true_labels, false_labels = dp.label_trips(true_trips, false_trips)


    # Create training matrix and labels.
    training = zip(true_trips, true_labels) + zip(false_trips, false_labels)
    training = np.random.permutation(training)

    train_matrix = [n[0] for n in training]
    train_labels = [n[1] for n in training]
    

    ## svm and prediction ##################################################
    
    c = 1
    results = dp.run_SVM(train_matrix, train_labels, c, trips)

    return results
    

all_drivers = os.listdir('../drivers')
all_drivers = [int(n) for n in all_drivers]


file_name = 'submission_1.csv'

try:
    with open(file_name, 'rb') as f:
        pass
except:
    with open(file_name, 'wb') as f:
        pass


for n in all_drivers:
    
    results = predict(n)
    
    temp = []
    with open(file_name, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            temp.append(row)
    
    temp = temp[1:]
    for i in range(1, len(results)+1):
        temp.append([str(n)+'_'+str(i), results[i-1]])

    # Write predictions to csv. Final submission form.
    with open(file_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(['driver_trip', 'prob'])
        for row in temp:
            writer.writerow(row)
            
    print 'driver '+str(n)+' done. Total: '+str(all_drivers.index(n)+1)
