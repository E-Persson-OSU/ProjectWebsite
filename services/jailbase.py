""" imports list """
import http.client
from http.client import RemoteDisconnected
import json
import csv
import time
import random
import services.db as db
import os
from boto.s3.connection import S3Connection

"""global variables"""
conn = http.client.HTTPSConnection("jailbase-jailbase.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': '{}'.format(S3Connection(os.environ['X-RapidAPI-Key'])),
    'X-RapidAPI-Host': "jailbase-jailbase.p.rapidapi.com"
}

"""run this to search chosen jail for records containing first and last name"""
def searchjailbase(source_id, last_name, first_name=""):
    searcharg = ""
    if len(first_name) > 0:
        searcharg = "/search/?source_id={}&last_name={}&first_name={}".format(source_id, last_name, first_name)
    else:
        searcharg = "/search/?source_id={}&last_name={}".format(source_id, last_name)
    conn.request("GET", searcharg, headers=headers)
    data = ''
    while True:
        try:
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            data = json.loads(data)
            break
        except ValueError:
            print('Gateway Timeout, trying again...')

    return data

"""run this to get list of ohio jails"""
def getsourceids():
    try:
        conn.request("GET", "/sources/", headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        data = json.loads(data)
        sourceids = []
        records = data["records"]
        for record in records:
            sourceids.append(record["source_id"])  
    except:
        sourceids = ['ia-tcso']
    
      
    return sourceids

def getnamedict():
    name = []
    namedict = []
    with open('names.csv', newline='') as namefile:
        reader = csv.DictReader(namefile)
        for row in reader:
            name = [row['last_name'], row['first_name']]
            namedict.append(name)
    return namedict

"""grab recent from random sourceid and """
def getrecent():
    sourceids = getsourceids()
    random_id = random.choice(sourceids)
    attempts = 0
    while True:
        try:
            conn.request("GET", "/recent/?source_id={}".format(random_id), headers=headers)
            res = conn.getresponse()
            data = res.read()
            data = data.decode("utf-8")
            data = json.loads(data)
            break   
        except (json.decoder.JSONDecodeError, http.client.ResponseNotReady) :
            print("Server error 500, trying again")
            random_id = random.choice(sourceids)
            time.sleep(2)
            attempts = attempts + 1
            if attempts > 2:
                random_id = "ia-tcso"
                data = json.loads()
                break
    
    records = data["records"]
    return records


def main(args):
    namedict = []
    name = ["",""]
    args.pop(0)
    if len(args) == 2:
        name[0] = (args[0])
        name[1] = (args[1])
    elif len(args) == 1:
        name[0] = (args[0])
    namedict.append(name)

    sourceidlist = getsourceids()
    bookinglist = []
    
    for sourceid in sourceidlist:
        print("Now searching {} for {}, {}".format(sourceid, name[0], name[1]))
        record = searchjailbase(sourceid,name[0],name[1])
        if len(record['records']) > 0:
            for booking in record['records']:
                bookinglist.append(booking)
    print(bookinglist)
