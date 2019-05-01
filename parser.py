"""
This script is parsing data exported from Apple Health app in order to count steps made per day. The number of steps is then writen into a CSV file. Some mock data could be found on my GitHub: github.com/hsarka
A blog post with visualization could be seen on my blog sarka.hubacek.uk 
"""

import xmltodict
import csv

with open("healthMockData.xml") as fd:
	doc = xmltodict.parse(fd.read())

doc["HealthData"]

# recordList contains only data from this part of the xml file
recordList = doc["HealthData"]["Record"]

# making an empty dictionary to fill up later with dates and steps
records = {}

# iterating record by record in recordList to find the "step count" records
for record in recordList:
	# choosing only the record type "step count"
	if record["@type"] == "HKQuantityTypeIdentifierStepCount":
		# strip the date to YYYY-MM-DD format
		tempKey = "%.10s" % record["@startDate"]
		# if the key is in records dict, add new value to the current value
		if tempKey in records:
			records[tempKey] = int(records[tempKey]) + int(record["@value"])
		# if the key is not there yet, make a new entry
		else:
			records[tempKey] = int(record["@value"])

# write parsed data to CSV file
header = ["date", "steps"]
with open("stepCountMockData.csv", mode="w") as f:
	writer = csv.writer(f, delimiter=",")
	writer.writerow(header)
	for key in records.keys():
		f.write("%s,%s\n"%(key,records[key]))