#!/usr/bin/python

r"""
	Author:  Elizabeth Peele Mumpower
	Date:  May 23rd, 2017
	Purpose:  Parse serials for Hathi Trust Report
"""

import os
import os.path
import sys 
import re
import requests
import xml.etree.ElementTree as ET


####Pull analytics query & iterate over MMSId only

def get_mms():
	mms = {'path': '/shared/Emory University Libraries/Reports/EPEELE/HathiSerial', 'apikey': 'l7xx00334afab90e47c9aa950cdc92b405b9', 'limit': '25'}
	r = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports?', params=mms)
	items = r.text

	tree = ET.ElementTree(ET.fromstring(items))
#mms_bib = []
	for item in tree.iterfind('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Column5'):
		yield item.text
	# if item not seen in mms_bib
	# 	mms_bib.append(item.text)
		

#print get_mms()

####Run MMSId's through bib API

# for bib in get_mms():
# 	try:
# 		bibs = {"mms_id": bib, "apikey": "l7xx7ed1d73cf63d4105a2cf1df41632344f"}
# 		r = requests.get('https://api-eu.hosted.exlibrisgroup.com/almaws/v1/bibs', params=bibs)
# 		bib_output = r.text
# 	except requests.exceptions.RequestException as e:
# 		sys.stderr.write(e)
# 				#print e
# 		sys.exit(1)



	# print bib_output

### Parse out fields from bib API

###Output to TSV file