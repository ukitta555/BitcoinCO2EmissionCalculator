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

client = MongoClient("mongourl")
print("Connection Successful")
mydb = client["dbname"]
mycol = mydb["collection_a"]

app = Flask(__name__)
app.json_encoder = MyEncoder


@app.route("/")
def homepage():
    return "Welcome"

@app.route("/getblock")
def fetchstore():
    try:
        client = MongoClient("mongourl")
        mydb = client["dbname"]
        mycol = mydb["collectionname"]
        api_url = "https://api.blockcypher.com/v1/btc/main/blocks/0000000000000000000899a1745839ff32b4ed130580db1c3e37c4ed557cbca5"
        headers = {'Content-type': 'application/json'}
        result = requests.get(url= api_url,headers = headers)
        data = result.json()

        response = {'blockhash': data['hash'], 'IP': data['relayed_by']}
        print(response)
        
        return "success"


    except:
        return "nope" 

   
@app.route("/fetchAll")          
def fetchall():
    try:
        client = MongoClient("mongourl")   
        mydb = client["dbname"]
        mycol = mydb["collectionname"]
        for x in mycol.find():
            print(jsonify(x).response)
        print(x)    
        return  "ok"      

    except:
        return "cannot fetch"   


if __name__ == "__main__":
    app.run(debug=True)