import requests
import json

url = " http://127.0.0.1:5000/webhook"

data = {"blockchain": "Main", "data":"get shit done"}

r = requests.post(url,data = json.dumps(data), headers={'Content-Type' : 'application/json'})

curl 'https://api.blockcypher.com/v1/btc/main/blocks/685181;685182;685183'