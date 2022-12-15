from asyncio import run_coroutine_threadsafe
from multiprocessing import pool
from pydoc import resolve
import re
from sqlite3 import Timestamp
from urllib import response
from pymongo import MongoClient
import requests
import json
from bson.json_util import ObjectId
import urllib
import urllib.request
from bson.json_util import dumps
import simplejson as json
import pandas as pd
import datetime
import time
    

class MyEncoder(json.JSONEncoder):   #JSON encoder class for handling json datatypes

        def default(self, obj):
            if isinstance(obj, ObjectId):
                return str(obj)
            return super(MyEncoder, self).default(obj)

client = MongoClient("mongodb://127.0.0.1:27017")
print('db connected')
mydb = client["POOLS_BTC"]
mycol = mydb["mycollection"]
x=715988  #set the blockheight range here (to not overload the api engine, we shouldn't try more than 2000 records at a time)
while x!=716489:

    z=x


    url= "https://chain.api.btc.com/v3/block/"+ str(z) +","+ str(z+1)+","+str(z+2)+","+str(z+3)+","+str(z+4)+","+str(z+5)+","+str(z+6)+","+str(z+7)+","+str(z+8)+","+str(z+9)
    x=x+10 



    headers = {'content-type' : 'application/json'}
    result = requests.get(url, headers=headers)
    response=result.json() #store the data as json
    
    #handle and clean the data, with the parameters we require for our calculations
    for item in response: 
        blockhash = response['data'][0]['hash']
        height = response['data'][0]['height']
        timestamp = response['data'][0]['timestamp']
        pool_name = response['data'][0]['extras']['pool_name']
        link = response['data'][0]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S")
        difficulty= response['data'][0]['difficulty']  
        pool_info1 = {'blockhash' : blockhash,'height': height,
                'Timestamp' : datetime_str,'difficulty': difficulty,
                'poolname': pool_name,'pool_link': link}
    #print(pool_info1)
    #print(type(pool_info1))
    for item in response:
        blockhash = response['data'][1]['hash']
        height = response['data'][1]['height']
        timestamp = response['data'][1]['timestamp']
        pool_name = response['data'][1]['extras']['pool_name']
        link = response['data'][1]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][1]['difficulty'] 
        pool_info2 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info2)
    #print(type(pool_info2))

    for item in response:
        blockhash = response['data'][2]['hash']
        height = response['data'][2]['height']
        timestamp = response['data'][2]['timestamp']
        pool_name = response['data'][2]['extras']['pool_name']
        link = response['data'][2]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][2]['difficulty'] 
        pool_info3 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info3)

    for item in response:
        blockhash = response['data'][3]['hash']
        height = response['data'][3]['height']
        timestamp = response['data'][3]['timestamp']
        pool_name = response['data'][3]['extras']['pool_name']
        link = response['data'][3]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][3]['difficulty'] 
        pool_info4 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info4)

    for item in response:
        blockhash = response['data'][4]['hash']
        height = response['data'][4]['height']
        timestamp = response['data'][4]['timestamp']
        pool_name = response['data'][4]['extras']['pool_name']
        link = response['data'][4]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][4]['difficulty'] 
        pool_info5 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info5)

    for item in response:
        blockhash = response['data'][5]['hash']
        height = response['data'][5]['height']
        timestamp = response['data'][5]['timestamp']
        pool_name = response['data'][5]['extras']['pool_name']
        link = response['data'][5]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][5]['difficulty'] 
        pool_info6 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info6)

    for item in response:
        blockhash = response['data'][6]['hash']
        height = response['data'][6]['height']
        timestamp = response['data'][6]['timestamp']
        pool_name = response['data'][6]['extras']['pool_name']
        link = response['data'][6]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][6]['difficulty'] 
        pool_info7 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info7)

    for item in response:
        blockhash = response['data'][7]['hash']
        height = response['data'][7]['height']
        timestamp = response['data'][7]['timestamp']
        pool_name = response['data'][7]['extras']['pool_name']
        link = response['data'][7]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][7]['difficulty'] 
        pool_info8 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info8)

    for item in response:
        blockhash = response['data'][8]['hash']
        height = response['data'][8]['height']
        timestamp = response['data'][8]['timestamp']
        pool_name = response['data'][8]['extras']['pool_name']
        link = response['data'][8]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][8]['difficulty'] 
        pool_info9 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    #print(pool_info9)

    for item in response:
        blockhash = response['data'][9]['hash']
        height = response['data'][9]['height']
        timestamp = response['data'][9]['timestamp']
        pool_name = response['data'][9]['extras']['pool_name']
        link = response['data'][9]['extras']['pool_link']
        converted_time = datetime.datetime.fromtimestamp(timestamp)
        datetime_str = converted_time.strftime( "%m/%d/%Y,  %H:%M:%S") 
        difficulty= response['data'][9]['difficulty'] 
        pool_info10 = {'blockhash' : blockhash,'height': height,
        'Timestamp' : datetime_str,'difficulty': difficulty, 
        'poolname': pool_name,'pool_link': link}
    print(pool_info10)

    mycol.insert_one(pool_info1)

    mycol.insert_one(pool_info2)

    mycol.insert_one(pool_info3)

    mycol.insert_one(pool_info4)

    mycol.insert_one(pool_info5)

    mycol.insert_one(pool_info6)
    mycol.insert_one(pool_info7)
    mycol.insert_one(pool_info8)
    mycol.insert_one(pool_info9)
    mycol.insert_one(pool_info10)
    print('insertions ok')  #insert to collection
    time.sleep(8) #put a sleep timer on the loop to pace the api calls

    
            

#
#mongoexport --db=dbname --collection=collectionname --type=csv --fields=_id,blockhash,height,Timestamp,difficulty,poolname,pool_link --out=outputfile.csv

#^this command is for exporting the data as a csv file (use --type=json for json format)