import logging
from datetime import datetime

from django.db.models import QuerySet

from src.bitcoin_emissions.consts import HOURS_IN_A_DAY, UNKNOWN_CO2_EMISSIONS_FACTOR, TONNE_MULTIPLIER, \
    UNKNOWN_POOL_LOCATION, UNKNOWN_POOL
from src.bitcoin_emissions.models import MiningGear, PoolLocation, AverageEfficiency, Pool, HashRatePerPoolServer, \
    Location

logger = logging.getLogger(__name__)


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
        AverageEfficiency.objects.create(
            date=calculation_date,
            average_efficiency_j_gh=average_gear_efficiency_j_gh
        )
        logger.info(f"Saved average gear efficiency for date {calculation_date}: {average_gear_efficiency_j_gh}")

        electricity_consumption_kwh_day = dict()
        co2_emissions_tco2e_day = dict()

        electricity_consumption_kwh_day[UNKNOWN_POOL_LOCATION] = 0
        co2_emissions_tco2e_day[UNKNOWN_POOL_LOCATION] = 0

        # TODO: remove logic for counting hashrate per server to other module; S from SOLID!
        unknown_and_unrecognized_servers_hash_rate = 0

        """
            Calculate location electricity usage and CO2 emissions by going through all pools 
        """
        for pool_name, pool_hash_rate_eh_s in pool_hash_rates.items():
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
                        pool_hash_rate_eh_s=pool_hash_rate_eh_s,
                        pool_servers_amount=1
                    )

                electricity_consumption_kwh_day[UNKNOWN_POOL_LOCATION] += electricity_consumption_for_pool
                co2_emissions_tco2e_day[UNKNOWN_POOL_LOCATION] += \
                    cls.get_co2_emissions(
                        electricity_consumption_for_server=electricity_consumption_for_pool,
                        emissions_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
                    )
                logger.info(f"No info about pool f{pool_name}; adding {pool_hash_rate_eh_s} to unknown sources")
                unknown_and_unrecognized_servers_hash_rate += pool_hash_rate_eh_s

            pool_object = Pool.objects.filter(pool_name=pool_name)

            for pool_server in pool_servers:

                def get_server_location_name(pool_server):
                    return pool_server.blockchain_pool_location.location_name

                def get_server_location(pool_server):
                    return pool_server.blockchain_pool_location

                pool_server_location = get_server_location_name(pool_server)

                if pool_name != UNKNOWN_POOL:
                    location_obj = get_server_location(pool_server)
                    HashRatePerPoolServer.objects.create(
                        blockchain_pool=pool_object[0],
                        blockchain_pool_location=location_obj,
                        hash_rate=pool_hash_rate_eh_s / pool_servers.count(),
                        date=calculation_date
                    )
                    logger.info(f"Saved hash rate information for pool {pool_name} servers "
                                f"at {pool_server_location} on {calculation_date}: "
                                f"{pool_hash_rate_eh_s / pool_servers.count()}")
                else:
                    unknown_and_unrecognized_servers_hash_rate += pool_hash_rate_eh_s

                if electricity_consumption_kwh_day.get(pool_server_location) is None:
                    electricity_consumption_kwh_day[pool_server_location] = 0
                if co2_emissions_tco2e_day.get(pool_server_location) is None:
                    co2_emissions_tco2e_day[pool_server_location] = 0

                electricity_consumption_for_server = \
                    cls.get_electricity_usage(
                        average_gear_efficiency_j_gh=average_gear_efficiency_j_gh,
                        pool_hash_rate_eh_s=pool_hash_rate_eh_s,
                        pool_servers_amount=pool_servers.count()
                    )

                electricity_consumption_kwh_day[pool_server_location] += electricity_consumption_for_server

                co2_emissions_tco2e_day[pool_server_location] += \
                    cls.get_co2_emissions(
                        electricity_consumption_for_server=electricity_consumption_for_server,
                        emissions_factor=pool_server.emission_factor
                    )

        HashRatePerPoolServer.objects.create(
            blockchain_pool=Pool.objects.get(pool_name=UNKNOWN_POOL),
            blockchain_pool_location=Location.objects.get(location_name=UNKNOWN_POOL_LOCATION),
            hash_rate=unknown_and_unrecognized_servers_hash_rate,
            date=calculation_date
        )
        logger.info(f"Saved hash rate information for unknown servers "
                    f"on {calculation_date}: "
                    f"{unknown_and_unrecognized_servers_hash_rate}")

        return electricity_consumption_kwh_day, co2_emissions_tco2e_day

    @classmethod
    def get_electricity_usage(cls, average_gear_efficiency_j_gh, pool_hash_rate_eh_s, pool_servers_amount):
        # 1000000000 * eh_s / 1000 -> 1000000 * eh_s -> gh_s
        return (1000000 * pool_hash_rate_eh_s) * HOURS_IN_A_DAY * average_gear_efficiency_j_gh / pool_servers_amount

    @classmethod
    def get_co2_emissions(cls, electricity_consumption_for_server, emissions_factor):
        return (electricity_consumption_for_server * emissions_factor) / TONNE_MULTIPLIER
