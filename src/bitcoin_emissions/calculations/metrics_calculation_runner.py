import enum
import json
import logging
from collections import deque
from datetime import datetime, timedelta
from fractions import Fraction
import time

import pandas as pd
import pytz
import requests
from django.core import exceptions

from src.bitcoin_emissions.calculations.helper_calculators.electicity_and_co2_usage_calculator \
    import ElectricityAndCO2Calculator
from src.bitcoin_emissions.calculations.helper_calculators.hashrate_calculator import HashRateCalculator
from src.bitcoin_emissions.consts import KWH_TO_GWH_MULTIPLIER, UNKNOWN_POOL
from src.bitcoin_emissions.models import BlocksFoundByPoolPerWindow, Pool, \
    PoolElectricityConsumptionAndCO2EEmissionHistory, Location
from src.bitcoin_emissions.models.co2_electricity_history_per_server_db_model import CO2ElectricityHistoryPerServer
from src.bitcoin_emissions.models.pool_locations_db_model import PoolLocation


logger = logging.getLogger(__name__)

class BeforeOrAfter(enum.Enum):
    BEFORE = 0
    AFTER = 1

class MetricsCalculationRunner:

    @classmethod
    def calculate_metrics_for_date_range(cls, start_date: datetime, end_date: datetime | None = None):
        date_to_fetch_blocks_for = start_date
        current_date = datetime.today()
        if end_date is None:
            end_date = current_date
        else:
            end_date = end_date
        rolling_window = deque(maxlen=720)

        unknown_pools = set()
        while date_to_fetch_blocks_for <= end_date:
            api_response = cls._get_blocks_for_date(
                date_to_fetch_blocks_for=date_to_fetch_blocks_for
            )

            if not api_response:
                continue

            oldest_block_height = api_response[-1]["height"]
            latest_block_height = api_response[0]["height"]

            logger.info(f"Fetched info for blocks "
                  f"({oldest_block_height}, "
                  f"{latest_block_height}), "
                  f"date {date_to_fetch_blocks_for}")

            """
                When deque grows to more than 720 elements, 
                old blocks will be automatically popped out
            """
            cleansed_block_range_date = cls._fetch_block_info_from_api_response(
                block_interval=api_response
            )
            rolling_window.extendleft(reversed(cleansed_block_range_date))

            if len(rolling_window) < 720:
                logger.info(
                    f"Length of rolling window at date {date_to_fetch_blocks_for} "
                    f"is less than 720: {len(rolling_window)}. "
                    f"Fetching blocks from the past to get 720 blocks."
                )

                interval_start = max(latest_block_height - 719, 0)

                block_interval = cls._fetch_interval_of_blocks(
                    start=interval_start,
                    end=oldest_block_height - 1
                )

                cleansed_block_range = cls._fetch_block_info_from_api_response(
                    block_interval=block_interval
                )
                rolling_window.extend(reversed(cleansed_block_range))

            assert cls._validate_rolling_window(rolling_window), \
                "Rolling window invariant broken!"
            assert len(rolling_window) == 720, \
                "Rolling window should always have 720 elements when switching to a new date!"  


            cls._save_info_about_rolling_window(
                rolling_window=rolling_window,
                end_date=date_to_fetch_blocks_for,
                unknown_pools=unknown_pools
            )

            hash_rates = HashRateCalculator.calculate_hash_rates_per_pool(
                rolling_window=rolling_window,
                date=date_to_fetch_blocks_for
            )
            electricity, co2_emissions, granural_emissions = ElectricityAndCO2Calculator.calculate(
                pool_hash_rates=hash_rates,
                calculation_date=date_to_fetch_blocks_for
            )
            cls._save_info_about_co2_and_electricity(
                date=date_to_fetch_blocks_for,
                co2_data=co2_emissions,
                electricity_data=electricity,
                granural_data=granural_emissions
            )
            logger.info(f"Sum of co2e emissions for date {date_to_fetch_blocks_for}:"
                  f" {sum([i for i in co2_emissions.values()])}"
            )
            date_to_fetch_blocks_for += timedelta(days=1)
        logger.info(unknown_pools)

    @classmethod
    def _get_closest_block_to_date(cls, date: datetime, before_or_after: BeforeOrAfter):
        result = requests.get(
            url=f"https://mempool.space/api/v1/mining/blocks/timestamp/"
                f"{int(date.timestamp())}",
            headers={"content-type": "application/json"})
        
        while result.status_code != 200:
            logger.info(f"Status code for fetching closest block to date: {result.status_code}.. sleeping for 2 seconds before retrying")
            time.sleep(2)
            result = requests.get(
                url=f"https://mempool.space/api/v1/mining/blocks/timestamp/"
                    f"{int(date.timestamp())}",
                headers={"content-type": "application/json"}
            )
        
        height = result.json().get("height")  # get dict representation of json response
        if height is not None:
            return height if before_or_after == BeforeOrAfter.BEFORE else height + 1 
        else:
            logger.info(f"Error while fetching the closest block for {date} date")
            raise Exception(f"Error while fetching the closest block for {date} date - no height provided by the API")

    @classmethod
    def _get_blocks_for_date(cls, date_to_fetch_blocks_for):
        # For future me: we had to replace btc.com API since it was really instable in terms of availability.

        # result = requests.get(
        #     url=f"https://chain.api.btc.com/v3/block/date/"
        #         f"{date_to_fetch_blocks_for.strftime('%Y%m%d')}",
        #     headers={"content-type": "application/json"})
        # data = result.json().get("data")  # get dict representation of json response
        # if data:
        #     return data
        # else:
        #     logger.info(f"No blocks were mined on {date_to_fetch_blocks_for}")
        start_block_height_for_the_date = cls._get_closest_block_to_date(
            date=date_to_fetch_blocks_for,
            before_or_after=BeforeOrAfter.AFTER
        )
        end_block_height_for_the_date = cls._get_closest_block_to_date(
            date=date_to_fetch_blocks_for + timedelta(days=1),
            before_or_after=BeforeOrAfter.BEFORE
        )
        logger.info(f"Fetching block range {start_block_height_for_the_date}-{end_block_height_for_the_date}")
        result = cls._fetch_interval_of_blocks(
            start=start_block_height_for_the_date,
            end=end_block_height_for_the_date
        )
        return list(reversed(result))

    @classmethod
    def _fetch_interval_of_blocks(cls, start: int, end: int):
        result = deque()
        # +1 for the interval [start, end] to be inclusive
        for starting_block_of_a_chunk in range(start, end + 1, 15):
            # (0,16) -> (0, 14) + (15, 16)
            ending_block_of_a_chunk = min(starting_block_of_a_chunk + 14, end) 
            print(starting_block_of_a_chunk, ending_block_of_a_chunk)
            
            logger.info(f"Trying to fetch information about next {ending_block_of_a_chunk - starting_block_of_a_chunk + 1} blocks...")
            api_response = requests.get(
                f"https://mempool.space/api/v1/blocks/{ending_block_of_a_chunk}",
                headers={"content-type": "application/json"}
            )

            while api_response.status_code != 200:
                logger.info(f"Status code is {api_response.status_code}, trying again after a 2 second sleep...")
                time.sleep(2)
                api_response = requests.get(
                    f"https://mempool.space/api/v1/blocks/{ending_block_of_a_chunk}",
                    headers={"content-type": "application/json"}
                )

            api_response = json.loads(api_response.text)
            
            if ending_block_of_a_chunk - starting_block_of_a_chunk + 1 == 15:
                logger.info(
                    f"Fetched info for blocks ("
                    f"{api_response[-1]['height']}, "
                    f"{api_response[0]['height']}) "
                    f"to fill the rolling window to 720 elements"
                )
                result.extend(reversed(api_response))
            else:
                api_response = list(reversed(api_response))
                logger.info(
                    f"Fetched info for blocks ("
                    f"{api_response[-(ending_block_of_a_chunk - starting_block_of_a_chunk + 1)]['height']},"
                    f"{api_response[-1]['height']}) "
                    f"to fill the rolling window to 720 elements"
                )
                result.extend(api_response[-(ending_block_of_a_chunk - starting_block_of_a_chunk + 1):])
        return result

    @classmethod
    def _fetch_block_info_from_api_response(cls, block_interval):
        blocks_info = []
        for block in block_interval:
            clean_block_info = {
                "height": block["height"],
                "difficulty": block["difficulty"],
                "pool_name": block["extras"]["pool"]["name"],
                "date": datetime.fromtimestamp(block["timestamp"]),
            }
            blocks_info.append(clean_block_info)
        return blocks_info

    @classmethod
    def _validate_rolling_window(cls, rolling_window):
        logger.info("Validating rolling window....")
        for i in range(len(rolling_window) - 1):
            if rolling_window[i]["height"] - rolling_window[i + 1]["height"] != 1:
                logger.info(f"Block {rolling_window[i + 1]['height']} "
                      f"and {rolling_window[i]['height']} "
                      f"in positions {i + 1} and {i} are not their in place.")
                return False
        logger.info("OK!")
        return True

    @classmethod
    def _save_info_about_rolling_window(cls, rolling_window: deque, end_date, unknown_pools: set):
        rolling_window_df = pd.DataFrame(rolling_window)
        block_found_by_each_pool = rolling_window_df.groupby("pool_name").size()
        unknown_blocks = 0
        for pool, blocks in block_found_by_each_pool.items():
            try:
                if pool != UNKNOWN_POOL:
                    pool_object = Pool.objects.get(pool_name=pool)
                    BlocksFoundByPoolPerWindow.objects.create(
                        blockchain_pool=pool_object,
                        window_start_date=rolling_window[-1]["date"],
                        window_end_date=end_date,
                        blocks_found=blocks
                    )
                else:
                    unknown_blocks += blocks
                    logger.info(
                        f"Unknown individual miners have mined {Fraction(blocks, len(rolling_window))} "
                        f"share of the rolling window."
                    )
            except exceptions.ObjectDoesNotExist:
                unknown_blocks += blocks
                unknown_pools.add(pool)
                # TODO: make this message more informative;
                # it is only displayed when there is no Pool object;
                # in case there is one but there is no server info, it won't be displayed.
                logger.info(
                    f"There is no information about pool {pool} in DB. "
                    f"Its share of rolling window is: {Fraction(blocks, len(rolling_window))}. "
                )
        unknown_pool = Pool.objects.get(pool_name=UNKNOWN_POOL)
        BlocksFoundByPoolPerWindow.objects.create(
            blockchain_pool=unknown_pool,
            window_start_date=rolling_window[-1]["date"],
            window_end_date=end_date,
            blocks_found=unknown_blocks
        )

    @classmethod
    def _save_info_about_co2_and_electricity(
            cls,
            date,
            electricity_data,
            co2_data,
            granural_data
        ):
        for location, co2_emissions in co2_data.items():
            electricity_usage = electricity_data[location]
            server_location_object = Location.objects.get(location_name=location)
            PoolElectricityConsumptionAndCO2EEmissionHistory.objects.create(
                date=date,
                electricity_usage=electricity_usage / KWH_TO_GWH_MULTIPLIER,
                co2e_emissions=co2_emissions,
                location_of_servers=server_location_object
            )

        for pool, server_emissions in granural_data.items():
            for servers_emission_record in server_emissions:
                server = PoolLocation.objects.filter(
                    blockchain_pool__pool_name=pool, 
                    blockchain_pool_location__location_name = servers_emission_record['server_location'],
                    # date__lte=date
                )[0]
                # print(server)
                CO2ElectricityHistoryPerServer.objects.create(
                    date=date,
                    electricity_usage=servers_emission_record['electricity'] / KWH_TO_GWH_MULTIPLIER,
                    co2e_emissions=servers_emission_record['co2_emissions'],
                    server_info=server
                )
