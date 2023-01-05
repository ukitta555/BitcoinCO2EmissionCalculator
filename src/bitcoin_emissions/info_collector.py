from datetime import datetime, timedelta
import time
from pprint import pprint

import requests
from src.bitcoin_emissions.consts import GENESIS_BLOCK_DATE
from collections import deque


class BlockFetcher:

    @classmethod
    def rolling_window_hashrate_calculation(cls):
        last_fetched_block = 0
        # date_to_fetch_blocks_for = GENESIS_BLOCK_DATE
        date_to_fetch_blocks_for = datetime(year=2021, month=5, day=1)
        current_date = datetime.today()
        rolling_window = deque(maxlen=720)

        pool_names = set()

        while date_to_fetch_blocks_for <= current_date:
            api_response = cls.get_blocks_for_date(
                date_to_fetch_blocks_for=date_to_fetch_blocks_for
            )
            date_to_fetch_blocks_for += timedelta(days=1)

            if not api_response:
                continue

            oldest_block_height_for_that_date = api_response[-1]["height"]
            latest_block_height_for_that_date = api_response[0]["height"]

            print(f"Fetched info for blocks "
                  f"({oldest_block_height_for_that_date}, "
                  f"{latest_block_height_for_that_date})")

            """
                When deque grows to more than 720 elements, 
                old blocks will be automatically popped out
            """
            cleansed_block_range_date = cls.fetch_block_info_from_api_response(
                block_interval=api_response
            )
            rolling_window.extendleft(reversed(cleansed_block_range_date))

            for block in cleansed_block_range_date:
                if not block["pool_name"] in pool_names:
                    pool_names.add(block["pool_name"])
                    print(f"Added pool {block['pool_name']} on date {date_to_fetch_blocks_for}")

            if latest_block_height_for_that_date >= 719:
                pass
                # interval_start = max(
                #     latest_block_height_for_that_date - 719,
                #     last_fetched_block
                # )

                # block_interval = cls.fetch_interval_of_blocks(
                #     start=interval_start,
                #     end=oldest_block_height_for_that_date
                # )


                # cleansed_block_range = cls.fetch_block_info_from_api_response(
                #     block_interval=block_interval
                # )
                # rolling_window.extendleft(cleansed_block_range)
                # last_fetched_block = latest_block_height_for_that_date
                # pprint(rolling_window)
            else:
                print(f"Latest block for date "
                      f"{date_to_fetch_blocks_for - timedelta(days=1)} is less than 719: "
                      f"{latest_block_height_for_that_date}")

            # time.sleep(0.5)
        print(pool_names)



    @classmethod
    def get_blocks_for_date(cls, date_to_fetch_blocks_for):
        result = requests.get(
            url=f"https://chain.api.btc.com/v3/block/date/"
                f"{date_to_fetch_blocks_for.strftime('%Y%m%d')}",
            headers={"content-type": "application/json"})
        data = result.json().get("data")  # get dict representation of json response
        if data:
            return data
        else:
            print(f"No blocks were mined on {date_to_fetch_blocks_for}")

    # clean the block data that we need for our calculations
    @classmethod
    def fetch_block_info_from_api_response(cls, block_interval):
        blocks_info = []
        for block in block_interval:
            blockhash = block["hash"]
            height = block["height"]
            timestamp = block["timestamp"]
            pool_name = block["extras"]["pool_name"]
            link = block["extras"]["pool_link"]
            datetime_str = datetime.fromtimestamp(timestamp).strftime("%m/%d/%Y,  %H:%M:%S")
            difficulty = block["difficulty"]
            clean_block_info = {
                "height": height,
                # "difficulty": difficulty,
                "pool_name": pool_name,
                # "pool_link": link,
            }
            blocks_info.append(clean_block_info)
        return blocks_info

    @classmethod
    def fetch_interval_of_blocks(cls, start: int, end: int):
        # +1 for the interval [start, end] to be inclusive
        # reverse order so that we can have the data structure
        # always sorted in "latest blocks first" order without sorting on our side

        result = deque()
        for block_chunk in range(start, end + 1, 50):
            blocks_to_fetch = ",".join(
                [str(i) for i in range(block_chunk, min(block_chunk + 50, end + 1))]
            )
            api_response = requests.get(
                f"https://chain.api.btc.com/v3/block/{blocks_to_fetch}",
                headers={"content-type": "application/json"}
            ).json()
            print(
                f"Fetched info for blocks ("
                f"{api_response['data'][0]['height']}, "
                f"{api_response['data'][-1]['height']})"
            )
            result.extend(api_response["data"])
        return result



    @classmethod
    def get_latest_block_height(cls):
        result = requests.get(
            "https://chain.api.btc.com/v3/block/latest",
            headers={"content-type": "application/json"}
        ).json()
        api_response = result.get("data")
        return api_response["height"]


if __name__ == "__main__":
    latest_block = BlockFetcher.get_latest_block_height()
    print("latest block", latest_block)
    BlockFetcher.rolling_window_hashrate_calculation()