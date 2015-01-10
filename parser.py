#code parse the driver files into a list of list of lists
#then dump as multiple json files
#have driver directory one above directory containing this

import csv, os
import cPickle as pickle

driver_names = [name for name in os.listdir('../drivers')]

#2736 = 18*8*19 total driver files, which is why we have 19 json files
num_drivers = 2736
num_files = 57
num_drives_per_driver = 200


for i in range(num_files):
	driverData = []
	counter = 0

	for n in driver_names[i*(num_drivers/num_files):(i+1)*(num_drivers/num_files)]:
		drivesPerDriver = []
		
		for j in range(num_drives_per_driver):
			testf = open('../drivers/'+n+'/'+str(j+1)+'.csv', 'rb')
			reader = csv.reader(testf)
			next(reader)
			
			coordPerDrive = []
			for row in reader:
				coordPerDrive.append((float(row[0]), float(row[1])))
			
			drivesPerDriver.append(coordPerDrive)
			testf.close()
		driverData.append(drivesPerDriver)
		
		# update on progress
		counter += 1
		print counter, 'drivers have data parsed, pickle dump file', i, '/', num_files

	file = open('driverData_'+str(i)+'.p', 'w+')
	pickle.dump(driverData, file)
	file.close()
	print 'pickle dump file', i, 'finished.'

