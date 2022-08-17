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
mydb = client["BlockhashDB"]
mycol = mydb["table2"]        

cursor = mycol.find({})
for document in cursor:
    print(document)


print("fetch completed")    
