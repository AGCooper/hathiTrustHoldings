#!/usr/bin/python
r"""
Authors: Alex Cooper, Bernardo Gomez
Purpose: Parse the MARC for HathiTrust Mono reports
Date: 06/27/2017
"""

from pymarc import MARCReader
import re
import sys
import socks
import socket

def main():

    reader = MARCReader(sys.stdin)
    ocm = re.compile("^ocm\d")
    ocn = re.compile("^ocn\d")
    ocolc = re.compile("^\(OCoLC\)\d")
    aleph = re.compile("^\(Aleph\)\d")
    try:
        for record in reader:
            try:
                gov_pub = mmsid = oclc_no = aleph_no = description = condition = issn = ''
                descriptions = []
                delim = "	"
                holding = "CH"
            except:
                sys.stderr.write("reader failed" + "\n")
                continue

            # get mmsid
            try:
                if record['001'] is not None:
                    mmsid = record['001'].value()
                    mmsid = str(mmsid)
#                    print mmsid
            except:
                sys.stderr.write("could not get mmsid" + "\n")

            # get oclc number
            try:
                for f in record.get_fields('035'):
                    net_no = f['a']
                    if ocm.match(net_no): 
                        oclc_no = net_no
                        break
                    elif ocn.match(net_no): 
                        oclc_no = net_no
                        break
                    elif ocolc.match(net_no): 
                        oclc_no = net_no
                        break
                    else:
                        oclc_no = ''
                    if aleph.match(net_no):
                        aleph_no = net_no
                    else:
                        continue
            except:
                sys.stderr.write("could not get oclc_no" + "\n")

            # id govdocs
            try:
                if record['008'] is not None:
                    try:
                        gov_pub = record['008'].value()
                    except:
                        sys.stderr.write("could not parse 008 for " + mmsid + "\n")
                    try:
                        gov_pub = str(gov_pub)
                    except:
                        sys.stderr.write("could not write string for " + mmsid + "\n")
                        continue
                    gov_pub = gov_pub[28]
                    if gov_pub == 'f':
                        gov_pub = 1
                    else:
                        gov_pub = 0
            except:
                sys.stderr.write("could not parse record " + mmsid + "\n")

            # get issn
            try:
                if record['022'] is not None:
                    try:
                        issn = record['022']['a']
                    except:
                        sys.stderr.write("could not parse 022 for " + mmsid + "\n")
            except:
                sys.stderr.write("could not get issn" + "\n")

            # get item information
            try:
                for f in record.get_fields('999'):
                    if f['d'] is not None:
                        description = f['d']
                    else:
                        description = ''
                    descriptions.append(description)
            except:
                sys.stderr.wrtite("could not get item info" + "\n")

            # print results
            try:
                for d in descriptions:
                    sys.stdout.write(str(oclc_no) + delim + str(mmsid) + "," + str(aleph_no) + delim + str(holding) + delim + str(condition) + delim + str(d) + delim + str(issn) + delim + str(gov_pub) + "\n")
            except:
                sys.stderr.write("could not parse item list" + "\n")
    except:
        sys.stderr.write("could not read marc record" + "\n")

if __name__=="__main__":
    sys.exit(main())
