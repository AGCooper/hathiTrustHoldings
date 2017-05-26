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

#NS:  {urn:schemas-microsoft-com:xml-analysis:rowset}Row
# {urn:schemas-microsoft-com:xml-analysis:rowset}Column0
# {urn:schemas-microsoft-com:xml-analysis:rowset}Column1
# {urn:schemas-microsoft-com:xml-analysis:rowset}Column2
# {urn:schemas-microsoft-com:xml-analysis:rowset}Column3
# {urn:schemas-microsoft-com:xml-analysis:rowset}Column4
# {urn:schemas-microsoft-com:xml-analysis:rowset}Column5

####Pull analytics query & iterate over MMSId only

#def get_mms():
mms = {'path': '/shared/Emory University Libraries/Reports/EPEELE/HathiSerial', 'apikey': 'l7xx00334afab90e47c9aa950cdc92b405b9', 'limit': '25'}
r = requests.get('https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports?', params=mms)
items = r.content
	#return items
	
# tree = ET.ElementTree(ET.fromstring(items))

tree = ET.fromstring(items)

for rows in tree.findall(".//{urn:schemas-microsoft-com:xml-analysis:rowset}Row"):
	try:
		this_node=rows.find("{urn:schemas-microsoft-com:xml-analysis:rowset}Column2").text
	except:
		sys.stderr.write("couldn't find Column2."+"\n")
	
	print this_node


# #for child in tree.iter():
# #	print child.tag

# #print tree.getroot()

# for item in tree.findall('./ResultXML'):
# 	item_node = item.find('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Row').text
	#mms_id = item_node.text

	#print item_node

	#return mms_id

	# try:
	# 	rows=tree.findall('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Row')
	# except:
	# 	sys.stderr.write("couldn't find rows."+"\n")

	# mms_id = ""
	# network_number = ""
	# material_type = ""
	# issn = ""
	# aleph_number = ""

	# for this_row in rows:
	# 		column = ""
	# 		try:
	# 			this_node = this_row.find('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Column1')
	# 			mms_id = str(this_node.text)
	# 		except:
	# 			sys.stderr.write("couldn't find Column 1."+"\n")
	# 		try:
	# 			this_node = this_row.find('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Column2')
	# 			network_number = str(this_node.text)
	# 		except:
	# 			sys.stderr.write("couldn't find Column 2."+"\n")
	# 		try:
	# 			this_node = this_row.find('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Column3')
	# 			material_type = str(this_node.text)
	# 		except:
	# 			sys.stderr.write("couldn't find Column 3."+"\n")
	# 		try:
	# 			this_node = this_row.find('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Column4')
	# 			issn = str(this_node.text)
	# 		except:
	# 			sys.stderr.write("couldn't find Column 4."+"\n")
	# 		try:
	# 			this_node = this_row.find('.//{urn:schemas-microsoft-com:xml-analysis:rowset}Column5')
	# 			aleph_number = str(this_node.text)
	# 		except:
	# 			sys.stderr.write("couldn't find Column 5."+"\n")

	# column=str(mms_id + network_number + material_type + issn + aleph_number)
	# id_list = []
	# id_list.append(column)
	# return id_list
	
		
# 		return column
		
#print get_mms()
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