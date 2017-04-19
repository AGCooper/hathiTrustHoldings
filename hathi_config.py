#!/usr/bin/python

def deleted_config(I_need):

    URL=str('https://api-na.hosted.exlibrisgroup.com/almaws/v1/analytics/reports')
    PATH=str('/shared/Emory University Libraries/Reports/ACOOPE5/Deleted_bibs')
    APIKEY=str('l7xx00334afab90e47c9aa950cdc92b405b9')
    LIMIT=str('1000')
    if I_need == "url":
        return URL
    elif I_need == "path":
        return PATH
    elif I_need == "apikey":
        return APIKEY
    elif I_need == "limit":
        return LIMIT
