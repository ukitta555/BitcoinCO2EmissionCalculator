from datetime import datetime

from django.db.models import QuerySet
from numpy import mean

from src.bitcoin_emissions.consts import HOURS_IN_A_DAY, UNKNOWN_CO2_EMISSIONS_FACTOR, TONNE_MULTIPLIER
from src.bitcoin_emissions.models import MiningGear, PoolLocation


class ElectricityAndCO2Calculator:

    @classmethod
    def calculate(
            cls,
            pool_hash_rates: dict,
            calculation_date: datetime
    ):
        average_gear_efficiency_j_gh = MiningGear.objects\
            .find_average_gear_efficiency_for_date(
                date=calculation_date
            )
        electricity_consumption_gwh_day = dict()
        co2_emissions_tco2e_day = dict()

        electricity_consumption_gwh_day["unknown"] = 0
        co2_emissions_tco2e_day["unknown"] = 0

        for pool_name, pool_hash_rate_gh_s in pool_hash_rates.items():
            pool_servers = PoolLocation.objects.find_latest_pool_servers_info_for_date(
                date=calculation_date,
                pool=pool_name
            )

            def pool_is_unknown(pool_servers: QuerySet[PoolLocation]):
                return pool_servers.count() == 0

            if pool_is_unknown(pool_servers):
                """
                    Since we put all pools that we do not have info about and blocks mined 
                    by "unknown" individuals in the same bucket, 
                    it would make sense to assume that all of them use one virtual "megaserver" 
                """
                electricity_consumption_for_pool = \
                    cls.get_electricity_usage(
                        average_gear_efficiency_j_gh=average_gear_efficiency_j_gh,
                        pool_hash_rate_gh_s=pool_hash_rate_gh_s,
                        pool_servers_amount=1
                    )

                electricity_consumption_gwh_day["unknown"] += electricity_consumption_for_pool
                co2_emissions_tco2e_day["unknown"] += \
                    cls.get_co2_emissions(
                        electricity_consumption_for_server=electricity_consumption_for_pool,
                        emissions_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
                    )

            for pool_server in pool_servers:

                def get_server_location(pool_server):
                    return pool_server.blockchain_pool_location.location_name

                pool_server_location = get_server_location(pool_server)

                if electricity_consumption_gwh_day.get(pool_server_location) is None:
                    electricity_consumption_gwh_day[pool_server_location] = 0
                if co2_emissions_tco2e_day.get(pool_server_location) is None:
                    co2_emissions_tco2e_day[pool_server_location] = 0

                """
                   Calculate location electricity usage and CO2 emissions by going through all pools 
                """

                electricity_consumption_for_server = \
                    cls.get_electricity_usage(
                        average_gear_efficiency_j_gh=average_gear_efficiency_j_gh,
                        pool_hash_rate_gh_s=pool_hash_rate_gh_s,
                        pool_servers_amount=pool_servers.count()
                    )

                electricity_consumption_gwh_day[pool_server_location] += electricity_consumption_for_server

                co2_emissions_tco2e_day[pool_server_location] += \
                    cls.get_co2_emissions(
                        electricity_consumption_for_server=electricity_consumption_for_server,
                        emissions_factor=pool_server.emission_factor
                    )

        return electricity_consumption_gwh_day, co2_emissions_tco2e_day

    @classmethod
    def get_electricity_usage(cls, average_gear_efficiency_j_gh, pool_hash_rate_gh_s, pool_servers_amount):
        return HOURS_IN_A_DAY * pool_hash_rate_gh_s * average_gear_efficiency_j_gh / pool_servers_amount

    @classmethod
    def get_co2_emissions(cls, electricity_consumption_for_server, emissions_factor):
        return (electricity_consumption_for_server * emissions_factor) / TONNE_MULTIPLIER
