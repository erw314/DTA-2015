import csv, sys, json

num_drivers = 2
num_drives_per_driver = 200
allDriverData = []

for i in range(num_drivers):
	drivesPerDriver = []
	
	for j in range(num_drives_per_driver):
		testf = open('drivers/'+str(i+1)+'/'+str(j+1)+'.csv', 'rb')
		reader = csv.reader(testf)
		next(reader)
		
		coordPerDrive = []
		for row in reader:
			coordPerDrive.append((float(row[0]), float(row[1])))
		
		drivesPerDriver.append(coordPerDrive)
	allDriverData.append(drivesPerDriver)
	
print allDriverData[0][0][:10]

file = open('driverData.json', 'w+')
json.dump(allDriverData, file)
