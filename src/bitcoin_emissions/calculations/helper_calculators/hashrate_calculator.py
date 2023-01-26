import logging
from collections import deque
from datetime import datetime
from decimal import Decimal

import pandas as pd

from src.bitcoin_emissions.consts import AVERAGE_BLOCK_MINING_TIME_SECS, EXA_MULTIPLIER
from src.bitcoin_emissions.models import BitcoinDifficulty, NetworkHashRate

logger = logging.getLogger(__name__)


class HashRateCalculator:

    @classmethod
    def calculate_hash_rates_per_pool(
            cls,
            rolling_window: deque,
            date: datetime
    ):
        rolling_window_df = pd.DataFrame(rolling_window)
        avg_difficulty = cls.get_averaged_difficulty(rolling_window_df, date)
        pool_name_groups = rolling_window_df.groupby("pool_name")
        pool_hash_rates_ehs = dict()
        for pool_name in pool_name_groups.groups:
            pool_name_group = pool_name_groups.get_group(pool_name)
            pool_hash_rates_ehs[pool_name] = \
                (cls._get_share_of_mined_blocks_by_pool(pool_name_group, rolling_window_df) *
                 cls._get_network_hash_rate_ehs(avg_difficulty))

        NetworkHashRate.objects.get_or_create(
            date=date,
            network_hash_rate_eh_s=cls._get_network_hash_rate_ehs(avg_difficulty)
        )
        logger.info(f"Saved network hash rate "
                    f"for {date}: "
                    f"{cls._get_network_hash_rate_ehs(avg_difficulty)}")

        return pool_hash_rates_ehs

    @classmethod
    def get_averaged_difficulty(cls, rolling_window_df, date):
        difficulty_groups = rolling_window_df.groupby("difficulty")
        difficulty_moving_average = Decimal(0)

        for difficulty in difficulty_groups.groups:
            difficulty_group: pd.DataFrame = difficulty_groups.get_group(difficulty)
            difficulty_moving_average += Decimal(len(difficulty_group) * difficulty) / Decimal(len(rolling_window_df))

        BitcoinDifficulty.objects.get_or_create(
            difficulty=difficulty_moving_average,
            date=date
        )
        logger.info(f"Saved average bitcoin difficulty "
                    f"for {date}: "
                    f"{difficulty_moving_average}")

        return difficulty_moving_average

    @classmethod
    def _get_network_hash_rate_ehs(cls, avg_difficulty):
        return Decimal((avg_difficulty * 2 ** 32) / (AVERAGE_BLOCK_MINING_TIME_SECS * EXA_MULTIPLIER))

    @classmethod
    def _get_share_of_mined_blocks_by_pool(cls, pool_name_group, rolling_window_df):
        return Decimal(len(pool_name_group) / len(rolling_window_df))

