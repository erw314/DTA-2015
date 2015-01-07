import json

# 

def getAllDriverData():
	file = open('~/driverData.json', 'r')
	return json.load(file)

# Returns all of input driver's drives, which are 
def getAllTripsFromDriver():
	return None

# Returns specified drives from a driver
def getTripsFromDriver(driver_number, trip_indices):

# make Trip object