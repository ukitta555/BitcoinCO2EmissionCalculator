from datetime import datetime
import time
import requests

# clean the block data that we need for our calculations
def fetch_block_info_from_api_response(response, blocks=10):
    blocks_info = []
    for block in range(blocks):
        blockhash = response[block]["hash"]
        height = response[block]["height"]
        timestamp = response[block]["timestamp"]
        pool_name = response[block]["extras"]["pool_name"]
        link = response[block]["extras"]["pool_link"]
        datetime_str = datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y,  %H:%M:%S")
        difficulty = response[block]["difficulty"]
        clean_block_info = {
            "blockhash": blockhash,
            "height": height,
            "Timestamp": datetime_str,
            "difficulty": difficulty,
            "pool_name": pool_name,
            "pool_link": link,
        }
        blocks_info.append(clean_block_info)
    return blocks_info


# set the block_height range here
# (to not overload the api engine, we shouldn't try more than 2000 records at a time)

last_fetched_block = 0
block_range_per_call = 10
while last_fetched_block != 716489:
    blocks_to_fetch = ",".join(
        [
            str(i)
            for i in range(
                last_fetched_block, last_fetched_block + block_range_per_call
            )
        ]
    )
    last_fetched_block = last_fetched_block + block_range_per_call
    url = f"https://chain.api.btc.com/v3/block/{blocks_to_fetch}"
    headers = {"content-type": "application/json"}
    result = requests.get(url, headers=headers)
    api_response = result.json().get("data")  # get dict representation of json response

    block_range = fetch_block_info_from_api_response(response=api_response, blocks=10)
    time.sleep(2)  # put a sleep timer on the loop to pace the api calls
