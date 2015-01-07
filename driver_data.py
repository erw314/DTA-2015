import json

def getAllDriverData():
	file = open("~/driverData.json", "r")
	return json.load(file)

# Returns all of input driver's drives, which are 
getAllDrivesFromDriver()

