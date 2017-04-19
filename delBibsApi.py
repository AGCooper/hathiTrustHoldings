#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
   Author: Alex Cooper
   Date: April, 2017
   Purpose: Parse deleted bibs report for hathi trust 
"""
import os
import sys 
import re
import requests
import xml.etree.ElementTree as ET


def get_item_info(result_node,id_list):

    outcome=1
    try:
        rows=result_node.findall("Row")
    except:
        sys.stderr.write("couldn't find Rows."+"\n")
    mms_id=""
    material_type=""
    barcode=""
    bib_status=""
    other_number=""
    title=""
    description=""
    barcode=""
    oclc_number=""
    item_id=""
    delim="	"
    for this_row in rows:
        item_row=""
        try:
            this_node=this_row.find("Column1")
            bib_status=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column1."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column2")
            material_type=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column2."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column3")
            mms_id=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column3."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column4")
            other_number=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column4."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column5")
            title=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column5."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column6")
            barcode=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column6."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column7")
            description=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column7."+"\n")
            return id_list,outcome
        try:
            this_node=this_row.find("Column8")
            oclc_number=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column8."+"\n")
            return id_list,outcome
        item_row=str(bib_status + delim + material_type + delim + mms_id + delim + other_number + delim + title + delim + barcode + delim + description + delim + oclc_number + delim + "WD")
        id_list.append(item_row)
    return id_list

def analytics_xml(url,apikey,path,limit):

    payload = { 'apikey':apikey, 'path':path, 'limit':limit }
    try:
        r = requests.get(url,params=payload)
    except:
        sys.stderr.write("api request failed" + "\n")
    return_code = r.status_code
    if return_code == 200:
        response = r.content
    else:
        sys.stderr.write("FAILED(1)" + "\n")
        response = r.content
        sys.stderr.write(str(response) + "\n")
        return 1
    in_string = response
    in_string = in_string.rstrip("\n")
    in_string = in_string.replace(" xmlns=\"urn:schemas-microsoft-com:xml-analysis:rowset\"","")
    id_list = []
    try:
        tree = ET.fromstring(in_string)
    except:
        sys.stderr.write("parse failed(1)" + "\n")
        return 1
    try:
        result_node = tree.find("QueryResult/ResultXml/rowset")
    except:
        sys.stderr.write("parse failed(2)" + "\n")
        return 1
    try:
        rows=result_node.findall("Row")
    except:
        sys.stderr.write("couldn't find Rows."+"\n")
    oclc_number = ""
    for this_row in rows:
        item_row = ""
        try:
            this_node=this_row.find("Column8")
            oclc_number=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column8."+"\n")
        item_row = oclc_number
        id_list.append(item_row)
    target = open("/tmp/id_list.tsv", 'a')
    for ids in id_list:
        ids = str(ids)
        target.write(ids + "\n")
    target.close()
    target = open("/tmp/id_list.tsv", 'r')
    return target.read()

