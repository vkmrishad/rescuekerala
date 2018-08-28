# Dependencies - Requests, dateutil
# Python 2.7.15

# Expects a csv file's path containing volunteer details
# Fill in the credentials in line 55, and run the script

# Example usage: 
# python2 path/to/sms.py path/to/csvFile.csv

import calendar
import csv
import datetime
import sys
import time

import requests

from dateutil import parser

csvFile = sys.argv[1] #command line argument

if __name__ == "__main__":

	# csv file path not provided
	if len(sys.argv) < 1:
		sys.exit()	

	#stores failed sms
	failed = open("Failed",'w')	
	fin = open(csvFile,'r')

	# to avoid multiple sms to same mobile number
	mark = {}	

	for fields in csv.reader(fin):
		
		sendID = fields[0]
		timestamp = fields[8]
		mobile = fields[3]

		if mobile in mark:
			continue
		mark[mobile]=1

		if mobile.isdigit():
			try:
				# Converting timestamp to epoch 
				timestamp = parser.parse(timestamp)
				timestamp = calendar.timegm(timestamp.utctimetuple())

				# Preparing unique URL
				url = 'http://keralarescue.in/c/' + sendID + "/" + str(timestamp)[-4:]
				message = "Thank you for registering to volunteer. Please click here to confirm " + url
							
				payload = { 'username':'xxxxxxxx','password':'xxxxxxxx','message':message,'numbers':mobile}
				response  = requests.get('http://api.esms.kerala.gov.in/fastclient/SMSclient.php',params=payload)

			except KeyboardInterrupt:

				failed.write(mobile)
				sys.exit()

			except:
				
				failed.write(mobile)

	fin.close()
	failed.close()
