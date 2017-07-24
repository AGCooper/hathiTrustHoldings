#!/usr/bin/python
# -*- coding: utf-8 -*-
r"""
   Author: Alex Cooper
   Date: April, 2017
   Purpose: Parse deleted bibs report for hathi trust 
"""
import os
import os.path
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
    delim="	"
    for this_row in rows:
        mms_id=""
        location=""
        material_type=""
        barcode=""
        bib_status=""
        other_number=""
        title=""
        description=""
        barcode=""
        oclc_number=""
        item_id=""
        item_type=""
        holding="WD"
        aleph_no=""
        condition=""
        description=""
        issn=""
        gov_pub=""
        mono_type=""
        item_row=""
        try:
            this_node=this_row.find("Column1")
            bib_status=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column1."+"\n")
        try:
            this_node=this_row.find("Column2")
            material_type=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column2."+"\n")
        try:
            this_node=this_row.find("Column3")
            mms_id=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column3."+"\n")
        try:
            this_node=this_row.find("Column4")
            location=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column4."+"\n")
        try:
            this_node=this_row.find("Column5")
            description=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column5."+"\n")
        try:
            this_node=this_row.find("Column6")
            item_type=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column6."+"\n")
        try:
            this_node=this_row.find("Column7")
            mono_type=str(this_node.text)
        except:
            sys.stderr.write("couldn't find Column7."+"\n")
        try:
            this_node=this_row.find("Column8")
            aleph_no=str(this_node.text)
            if aleph_no.startswith("No"):
                aleph_no=""
        except:
            sys.stderr.write("couldn't find Column8."+"\n")
        try:
            this_node=this_row.find("Column9")
            oclc_number=str(this_node.text)
            if oclc_number.startswith("(OCoLC)9900"):
                oclc_number = ""
            elif oclc_number.startswith("No"):
                oclc_number = ""
        except:
            sys.stderr.write("couldn't find Column9."+"\n")
        item_row=str(oclc_number) + delim + str(mms_id) + "," + str(aleph_no) + delim + str(holding) + delim + str(condition) + delim + str(description) + delim + str(issn) + delim + str(gov_pub)
        id_list.append(item_row)
        outcome = 0
    return id_list,outcome

def analytics_xml(url,apikey,path,limit):

    file_name = "/tmp/id_list.tsv"
    if os.path.isfile(file_name):
        os.remove(file_name)
    else:
        do_nothing = True
    in_string = ""
    outcome = 1
    payload = { 'apikey':apikey, 'path':path, 'limit':limit }
    try:
        r = requests.get(url,params=payload)
    except:
        sys.stderr.write("api request failed" + "\n")
    return_code = r.status_code
    if return_code == 200:
        response = r.content
    else:
        sys.stderr.write("FAILED(1)\n")
        response=r.content
        sys.stderr.write(str(response)+"\n")
        return 1
    in_string=response
    in_string=in_string.replace("\n","")
    in_string=in_string.replace(" xmlns=\"urn:schemas-microsoft-com:xml-analysis:rowset\"","")
    try:
        tree=ET.fromstring(in_string)
    except:
        sys.stderr.write("parse failed(1a)."+"\n")
        return outcome
    try:
        finished=tree.find("QueryResult/IsFinished")
    except:
        sys.stderr.write("parse failed(2)."+"\n")
        return outcome
    id_list=[]
    if finished.text == "false":
        try:
            token=tree.find("QueryResult/ResumptionToken")
        except:
            sys.stderr.write("parse failed(3)."+"\n")
            return outcome
        this_token=str(token.text)
        id_list=[]
        sys.stderr.write(str(url)+" "+str(apikey)+" "+this_token+" "+str(id_list)+" "+limit+"\n")
        try:
            result_node=tree.find("QueryResult/ResultXml/rowset")
        except:
            sys.stderr.write("couldn't find rowset."+"\n")
            return outcome
        id_list,outcome=get_item_info(result_node,id_list)
        work_to_do=True
        outcome=1
        while work_to_do:
            payload={'apikey':apikey,'token':this_token,'limit':limit}
            try:
                r=requests.get(url,params=payload)
            except:
                sys.stderr.write("api request failed."+"\n")
                return outcome
            return_code=r.status_code
            if return_code == 200:
                response=r.content
            else:
                sys.stderr.write("FAILED(2)\n")
                response=r.content
                sys.stderr.write(str(response)+"\n")
                return outcome
            in_string=response
            in_string=in_string.replace("\n","")
            in_string=in_string.replace(" xmlns=\"urn:schemas-microsoft-com:xml-analysis:rowset\"","")
            try:
                tree=ET.fromstring(in_string)
            except:
                sys.stderr.write("parse failed(1.i)."+"\n")
                return outcome
            try:
                finished=tree.find("QueryResult/IsFinished")
            except:
                sys.stderr.write("parse failed(2)."+"\n")
                return outcome
            if finished.text == "true":
                work_to_do=False
            try:
                result_node=tree.find("QueryResult/ResultXml/rowset")
#                print result_node
            except:
                sys.stderr.write("couldn't find rowset."+"\n")
                return outcome
            id_list,outcome=get_item_info(result_node,id_list)
    else:
        try:
            result_node=tree.find("QueryResult/ResultXml/rowset")
        except:
            sys.stderr.write("couldn't find rowset."+"\n")
            return outcome
        id_list,outcome=get_item_info(result_node,id_list)
    target = open(file_name, 'w')
    for ids in id_list:
        target.write(ids + "\n")
    target.close
    return file_name
