from datetime import datetime

from django.db.models import Avg, Subquery
from numpy import mean

from src.bitcoin_emissions.consts import HOURS_IN_A_DAY
from src.bitcoin_emissions.models import MiningGear, PoolLocation


class ElectricityUsageCalculator:

    @classmethod
    def calculate_electricity_usage(
            cls,
            pool_hash_rates: dict,
            calculation_date: datetime
    ):
        average_gear_efficiency = cls._find_average_gear_efficiency_for_date(
            date=calculation_date
        )
        pool_electricity_consumption_per_server = dict()
        pool_server_amount = dict()
        for pool_name, pool_hashrate_gh in pool_hash_rates.items():
            pool_server_amount[pool_name] = cls._find_amount_of_pool_servers_for_date(
                date=calculation_date,
                pool=pool_name
            )
            #TODO: fix no data
            if pool_server_amount[pool_name] == 0:
                pool_electricity_consumption_per_server[pool_name] = "No data!"
            else:
                pool_electricity_consumption_per_server[pool_name] = \
                    HOURS_IN_A_DAY * pool_hashrate_gh * average_gear_efficiency / pool_server_amount[pool_name]
        return pool_electricity_consumption_per_server

    @classmethod
    def _find_average_gear_efficiency_for_date(cls, date):
        return mean(
            list(
                map(
                    lambda x: x.efficiency,
                    MiningGear.objects\
                        .filter(release_date__lte=date)\
                        .order_by("-release_date")[:3]
                )
            )
        )

    @classmethod
    def _find_amount_of_pool_servers_for_date(cls, date, pool):
        closest_date = PoolLocation.objects\
            .filter(valid_for_date__lte=date)\
            .order_by("-valid_for_date")[0].valid_for_date

        return PoolLocation.objects.filter(
            blockchain_pool__pool_name=pool,
            valid_for_date=closest_date
        ).count()




