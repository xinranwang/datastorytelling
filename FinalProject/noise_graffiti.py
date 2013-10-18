from datetime import datetime
from geopy.point import Point
from operator import itemgetter
import numpy as np
import matplotlib.nxutils as nx

if __name__ == '__main__':
	f = open('data/311_Service_Requests_from_2010_to_Present.csv')
	data = f.readlines()
	f.close()

	len(data)

	header_row = data[0]
	print header_row

	data = list(set(data)) # this is a hack!
	print len(data)

	lower_manhattan = np.array([
		[40.726809, -73.971311], 
		[40.744207, -74.013583], 
		[40.707618, -74.023968], 
		[40.698574, -74.018990], 
		[40.709375, -73.976590]], float)

	# Get Graffiti data
	graffitis = []
	for record in data:
	    if 'Graffiti' in record.split(',')[5]:
	        graffitis.append(record)

	# Get id, datetime, point(lat, lng)
	formatted_graffitis = []
	for record in graffitis:
	    array = record.split(',')
	    formatted_graffitis.append([array[0], 
	    	datetime.strptime(array[1], "%m/%d/%Y %I:%M:%S %p"), 
	    	Point((array[49], array[50]))])

	# Graffiti in 2013 w/ coordinates
	formatted_graffitis_2013 = []
	for record in formatted_graffitis:
	    if record[1].year == 2013 and nx.pnpoly(record[2].latitude, record[2].longitude, lower_manhattan) == 1:
	        formatted_graffitis_2013.append(record)

	# sort by time
	formatted_graffitis.sort(key=itemgetter(1), reverse=True)

	# get in months
	formatted_graffitis_2013_month_dict = {}
	for i in range(1, 13):
		l = []
		for record in formatted_graffitis_2013:
			if record[1].month == i:
				l.append(record)
		formatted_graffitis_2013_month_dict[i] = l

	# Get Noise Data
	noises = []
	for record in data:
	    if 'Noise' in record.split(',')[5]:
	        noises.append(record)

	complaint_type = set()
	descriptor = set()

	# Get Complaint Type and Descriptor for noise
	for record in noises:
	    complaint_type.add(record.split(',')[5])
	    descriptor.add(record.split(',')[6])

	# Get id, datetime, point(lat, lng), complaint_type, descriptor
	formatted_noises = []
	for record in noises:
		array = record.split(',')
		formatted_noises.append([array[0], 
		datetime.strptime(array[1], "%m/%d/%Y %I:%M:%S %p"), 
			Point((array[49], array[50])),
	    	array[5],
	    	array[6]])

	# Noises in 2013 w/ coordinates
	formatted_noises_2013 = []
	for record in formatted_noises:
	    if record[1].year == 2013 and nx.pnpoly(record[2].latitude, record[2].longitude, lower_manhattan) == 1:
	        formatted_noises_2013.append(record)

	# build a dict
	formatted_noises_2013_dict = {}

	for c in complaint_type:
		l = []
		for record in formatted_noises_2013:
			if record[3] == c:
				l.append(record)
		formatted_noises_2013_dict[c] = l

	for key, value in formatted_noises_2013_dict.iteritems():
		print key + ": " + str(len(value))

	# build a dict for all months in 2013
	formatted_noises_2013_month_dict = {}

	for i in range(1, 13):
		temp_dict = {}
		for key, value in formatted_noises_2013_dict.iteritems():
			l = []
			for record in value:
				if record[1].month == i:
					l.append(record)
			temp_dict[key] = l
		formatted_noises_2013_month_dict[i] = temp_dict

	for key, value in formatted_noises_2013_month_dict[8].iteritems():
		print key + ": " + str(len(value))





