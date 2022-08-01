##Start Mongodb server 
##run python3 api_call.py

from pydoc import resolve
import re
from urllib import response
from flask import Flask,Response, jsonify
from pymongo import MongoClient
import requests
import json
from bson.json_util import ObjectId
import urllib



class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(MyEncoder, self).default(obj)

client = MongoClient("mongodb://127.0.0.1:27017")
print("Connection Successful")
mydb = client["BlockhashDB"]
mycol = mydb["collection_a"]

app = Flask(__name__)
app.json_encoder = MyEncoder


@app.route("/")
def homepage():
    return "Welcome"

@app.route("/getblock")         ##returns 0000000000000000000899a1745839ff32b4ed130580db1c3e37c4ed557cbca5 block info
def fetchstore():
    try:
        client = MongoClient("mongodb://127.0.0.1:27017")
        mydb = client["BlockhashDB"]
        mycol = mydb["collection_1a"]
        api_url = "https://api.blockcypher.com/v1/btc/main/blocks/0000000000000000000899a1745839ff32b4ed130580db1c3e37c4ed557cbca5"
        headers = {'Content-type': 'application/json'}
        result = requests.get(url= api_url,headers = headers)
        data = result.json()

        response = {'blockhash': data['hash'], 'IP': data['relayed_by']}
        print(response)
        query = mycol.insert_one(response)
        print("insertion successful")
        print(response)
        print(client.list_database_names())
        print(mydb.list_collection_names())
        return "success"


    except:
        return "nope" 
@app.route("/getprevblock")   ## returns the latest block info and stores in mongodb
def getprev():
    client = MongoClient("mongodb://127.0.0.1:27017")
    mydb = client["BlockhashDB"]
    mycol = mydb["collection_1a"]

    try:
    
        bit_main_url = "https://api.blockcypher.com/v1/btc/main"
        headers= {'Content-type':'application/json'}
        result = requests.get(url=bit_main_url, headers = headers)
        data = result.json()

        latest_block = {'blockhash': data['hash']}
        print("lastest blockhash is", latest_block)
        y = latest_block.get('blockhash')
        print(y)
        blockhash_url = "https://api.blockcypher.com/v1/btc/main/blocks/" + y
        print(blockhash_url)
        headers= {'Content-type':'application/json'}
        result = requests.get(url=blockhash_url, headers = headers)
        data1 = result.json()
        print('latest block info fetched')
        x =  {'blockhash': data1['hash'], 'IP': data1['relayed_by']}
        print(x)
        a = mycol.insert_one(x)
        print('insertion ok')
        return x

    except:
        return "nope sorry"    

@app.route("/fetchAll")  ##get the collection of latest blocks and Ips        
def fetchall():
    try:
        client = MongoClient("mongodb://127.0.0.1:27017")   
        mydb = client["BlockhashDB"]
        mycol = mydb["collection_1a"]
        for x in mycol.find():
            print(jsonify(x).response)
        print(x)    
        return  "ok"      

    except:
        return "cannot fetch"   


if __name__ == "__main__":
    app.run(debug=True)
