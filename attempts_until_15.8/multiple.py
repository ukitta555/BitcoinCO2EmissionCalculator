from pydoc import resolve
import re
from urllib import response
from flask import Flask,Response, jsonify
from pymongo import MongoClient
import requests
import json
from bson.json_util import ObjectId
import urllib
from bson.json_util import dumps


class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)


client = MongoClient("mongodb://127.0.0.1:27017")

mydb = client["BlockhashDB"]
mycol = mydb["collection_b"]




app = Flask(__name__)
app.json_encoder = MyEncoder

url_latest = "https://api.blockcypher.com/v1/btc/main"
headers = {'content-type' : 'application/json'}
result = requests.get(url_latest, headers=headers)
a = result.json()
##b = {'blockhash': a['hash']}
##c = b.get('blockhash')


@app.route("/")
def homepage():
    return "Welcome"



@app.route("/getlatest")
def getlatest():
        try: 
            url_latest = "https://api.blockcypher.com/v1/btc/main"
            headers = {'content-type' : 'application/json'}
            result = requests.get(url_latest, headers=headers)
            a = result.json()
            b = {'blockhash': a['hash']}
            c = b.get('blockhash')
            url = "https://api.blockcypher.com/v1/btc/main/blocks/" + c          
            headers = {'content-type' : 'application/json'}
            result = requests.get(url, headers=headers)
            data = result.json()
            print("1")
            x = {'blockhash': data['hash'], 'IP': data['relayed_by']}
            print(x)
            a = mycol.insert_one(x)
            print("insertion done")
            return "yay"
            
        except:    
            return "nay"
@app.route("/getblockinfo")
def getinfo():
    try:
        global c
        
    except:
        return "nay"   
@app.route("/fetchAll")          
def fetchall():
    print(mydb.list_collection_names())
    try:
        for x in mycol.find():
            print(jsonify(x).response)
        return "yay"
    except:
        return "nay"        


if __name__ == "__main__":
    app.run(debug=True)