import json
import urllib.request

import requests
from bson.json_util import ObjectId
from pymongo import MongoClient


url = "https://api.blockcypher.com/v1/btc/main/blocks/685595;685596;685597"  ##Start from 480 ##pace yourself [200 reqs/hr or 60 batch calls/hr]
headers = {"content-type": "application/json"}
result = requests.get(url, headers=headers)
response = result.json()
# print(response)
# mylist = json.dumps(data)
# print(mylist)

for item in response:
    blockhash = format(item["hash"])
    IP = format(item["relayed_by"])
    timestamp = format(item["received_time"])

    block_info = {"blockhash": blockhash, "time": timestamp, "IP_Adress": IP}
    # print (block_info)
    for item in block_info:
        IP_full = block_info.get("IP_Adress")
        IP_sans_mining_node = IP_full[:-5]
        # print(IP_sans_mining_node)
        geo_api_url = "http://ip-api.com/json/"
        #
        req = urllib.request.Request(geo_api_url + IP_sans_mining_node)
        response = urllib.request.urlopen(req).read()
        json_res = json.loads(response.decode("utf-8"))
        # print(json_res)
        geo_info = {
            "Region": json_res["regionName"],
            "Country": json_res["country"],
            "Latitude": json_res["lat"],
            "Longitude": json_res["lon"],
        }
    def Merge(dict1, dict2):
        res = {**dict1, **dict2}
        return res

    mergedinfo = Merge(block_info, geo_info)
    print(mergedinfo)
