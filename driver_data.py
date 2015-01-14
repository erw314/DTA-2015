import json
from trip import Trip


def getAllDriverData():
	file = open('~/driverData.json', 'r')
	return json.load(file)

# Returns all of input driver's drives, which are 
def getAllTripsFromDriver():
	return None

# Returns specified drives from a driver
def getTripsFromDriver(driver_number, trip_indices):
	return None

# make Trip object
coordinates = [(0,0), (3,4), (4,5)]
trip = Trip(0, coordinates)
print trip.driver 

