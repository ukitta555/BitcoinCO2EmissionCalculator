from collections import deque
from decimal import Decimal, ROUND_DOWN

import pandas as pd

from src.bitcoin_emissions.consts import AVERAGE_BLOCK_MINING_TIME_SECS, GIGA_MULTIPLIER


class HashRateCalculator:

    @classmethod
    def calculate_hash_rates_per_pool(cls, rolling_window: deque):
        rolling_window_df = pd.DataFrame(rolling_window)
        avg_difficulty = cls.get_averaged_difficulty(rolling_window_df)

        pool_name_groups = rolling_window_df.groupby("pool_name")
        pool_hash_rates_ghs = dict()
        for pool_name in pool_name_groups.groups:
            pool_name_group = pool_name_groups.get_group(pool_name)
            pool_hash_rates_ghs[pool_name] = \
                (cls._get_share_of_mined_blocks_by_pool(pool_name_group, rolling_window_df) *
                 cls._get_network_hash_rate_ghs(avg_difficulty))\
                .quantize(Decimal('.0000001'), rounding=ROUND_DOWN)  # rounding for testing purposes
        return pool_hash_rates_ghs

    @classmethod
    def get_averaged_difficulty(cls, rolling_window_df):
        difficulty_groups = rolling_window_df.groupby("difficulty")
        difficulty_moving_average = 0

        for difficulty in difficulty_groups.groups:
            difficulty_group: pd.DataFrame = difficulty_groups.get_group(difficulty)
            difficulty_moving_average += (len(difficulty_group) * difficulty) / len(rolling_window_df)

        return Decimal(difficulty_moving_average)

    @classmethod
    def _get_network_hash_rate_ghs(cls, avg_difficulty):
        return Decimal((avg_difficulty * 2 ** 32) / (AVERAGE_BLOCK_MINING_TIME_SECS * GIGA_MULTIPLIER))

    @classmethod
    def _get_share_of_mined_blocks_by_pool(cls, pool_name_group, rolling_window_df):
        return Decimal(len(pool_name_group) / len(rolling_window_df))

