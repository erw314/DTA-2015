import csv

#change file names
f_orig = open('sampleSubmission.csv', 'r')
f_new = open('sampleSubmissionMod.csv', 'w')

reader = csv.reader(f_orig)
writer = csv.writer(f_new)
linenum = 0

for line in reader:
    if linenum == 0:
        writer.writerow(line)
        linenum += 1
    else:
        driver = line[0]
        prob = line[1]
        # change scaling function
        writer.writerow((driver, str(1-(1-float(prob))**2)))

f_orig.close()
f_new.close()
