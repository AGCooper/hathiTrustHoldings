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

# function to return an array from a file
def getContents(filename):
  with open(filename, 'r') as f:
    contents = f.read().splitlines()
  return contents

####Pull analytics query & iterate over MMSId only

tree = ET.parse('/Users/epeele/hathiTrustHoldings/HathiSerial.xml')

try:
	rows=tree.findall(".//{urn:schemas-microsoft-com:xml-analysis:rowset}R")
except:
	sys.stderr.write("couldn't find rows."+"\n")

#print rows

mms_id = ""
network_number = ""
material_type = ""
issn = ""
aleph_number = ""
delim = "	"

f = open("emory_serial.tsv", "w")

for this_row in rows:
	column = ""
	try:
		this_node = this_row.find(".//{urn:schemas-microsoft-com:xml-analysis:rowset}C0")
		mms_id = str(this_node.text)
	except:
		sys.stderr.write("couldn't find MMS Id."+"\n")
	try:
		this_node = this_row.find(".//{urn:schemas-microsoft-com:xml-analysis:rowset}C1")
		issn = str(this_node.text)
	except:
		sys.stderr.write("couldn't find ISSN."+"\n")
	try:
		this_node = this_row.find(".//{urn:schemas-microsoft-com:xml-analysis:rowset}C2")
		aleph_number = str(this_node.text)
	except:
		sys.stderr.write("couldn't find Aleph Number."+"\n")
	# try:
	# 	this_node = this_row.find(".//{urn:schemas-microsoft-com:xml-analysis:rowset}C3")
	# 	material_type = str(this_node.text)
	# except:
	# 	sys.stderr.write("couldn't find Column 4."+"\n")
	try:
		this_node = this_row.find(".//{urn:schemas-microsoft-com:xml-analysis:rowset}C3")
		network_number = str(this_node.text)
	except:
		sys.stderr.write("couldn't find OCLC Number."+"\n")


	column=(network_number + delim + mms_id + delim + aleph_number + delim + issn)
	id_list = []
	#id_list.append(column)
	#print id_list

	govdocs_num = getContents('/Users/epeele/hathiTrustHoldings/hathi-serial-govdocs.txt')
	#print govdocs_num

	if mms_id in govdocs_num:
		id_list.append(column + delim + '1')
	else:
		id_list.append(column + delim + '0')

	#print id_list
	for line in id_list:
		f.write("%s\n" % line)