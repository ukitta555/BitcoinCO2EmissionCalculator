import itertools
from blockcypher import get_blocks_overview
import json
from pydoc import resolve
import re
from urllib import response
from flask import Flask,Response, jsonify
from pymongo import MongoClient
import requests
import json
from bson.json_util import ObjectId
import urllib
import urllib.request
from bson.json_util import dumps
import simplejson as json
import jsonpickle


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)

client = MongoClient("mongodb://127.0.0.1:27017")
print('db connected')
mydb = client["DB_BTC"]
mycol = mydb["table_1"]

url = "https://api.blockcypher.com/v1/btc/main/blocks/685595;685596;685597"     ##Start from 480 ##pace yourself [200 reqs/hr or 60 batch calls/hr]     
headers = {'content-type' : 'application/json'}
result = requests.get(url, headers=headers)
response=result.json()
#print(response)
#mylist = json.dumps(data)
#print(mylist)

for item in response:
    blockhash = format(item["hash"])
    IP = format(item["relayed_by"])
    timestamp = format(item["received_time"]) 
   
    block_info = {"blockhash": blockhash, "time": timestamp, "IP_Adress":IP}
    #print (block_info)
    for item in block_info:
        IP_full = block_info.get('IP_Adress')
        IP_sans_mining_node = IP_full[:-5]
        #print(IP_sans_mining_node)
        geo_api_url = 'http://ip-api.com/json/'
        #
        req = urllib.request.Request(geo_api_url+IP_sans_mining_node)
        response = urllib.request.urlopen(req).read()
        json_res= json.loads(response.decode('utf-8'))
        #print(json_res)
        geo_info = {'Region':  json_res['regionName'], 'Country': json_res['country']  ,
                                'Latitude':json_res['lat'],
                                'Longitude': json_res['lon'] 
                            }
        #print(geo_info) 

    def Merge(dict1,dict2):
            res = {**dict1, **dict2}
            return res
    mergedinfo = Merge(block_info, geo_info) 
    print(mergedinfo)
    #print(type(mergedinfo))  
    mycol.insert_one(mergedinfo) 
    print("insertion ok")
    
    
    

