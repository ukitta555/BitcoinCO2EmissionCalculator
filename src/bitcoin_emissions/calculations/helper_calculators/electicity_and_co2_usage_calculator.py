from decimal import Decimal
import logging
from datetime import datetime
from typing import Any, Dict, List, Set, Union

from django.db.models import QuerySet

from src.bitcoin_emissions.consts import EXA_H_S_TO_GIGA_H_S_MULTIPLIER, HOURS_IN_A_DAY, KWH_MULTIPLIER, UNKNOWN_CO2_EMISSIONS_FACTOR, TONNE_MULTIPLIER, \
    UNKNOWN_POOL_LOCATION, UNKNOWN_POOL, UNRECOGNIZED_POOL
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

        # TODO: refactor to use classes?
        electricity_consumption_kwh_day = dict()
        co2_emissions_tco2e_day = dict()
        server_granural_information: Dict[str, List[Dict[str, Union[str, Decimal]]]] = dict()

        electricity_consumption_kwh_day[UNKNOWN_POOL_LOCATION] = 0
        co2_emissions_tco2e_day[UNKNOWN_POOL_LOCATION] = 0

        server_granural_information[UNKNOWN_POOL] = []
        server_granural_information[UNKNOWN_POOL].append(
            {
                'server_location': UNKNOWN_POOL_LOCATION,
                'co2_emissions': Decimal(0.000000),
                'electricity': Decimal(0.000000),
            }
        )

        server_granural_information[UNRECOGNIZED_POOL] = []
        server_granural_information[UNRECOGNIZED_POOL].append(
            {
                'server_location': UNKNOWN_POOL_LOCATION,
                'co2_emissions': Decimal(0.000000),
                'electricity': Decimal(0.000000),
            }
        )

        # TODO: remove logic for counting hashrate per server to other module; S from SOLID!
        unknown_servers_hash_rate = 0
        unrecognized_servers_hash_rate = 0

        """
            Calculate location electricity usage and CO2 emissions by going through all pools 
        """
        for pool_name, pool_hash_rate_eh_s in pool_hash_rates.items():

            # always use closest sheet of data; if server is not present there, pushes the results to unrecognized servers
            pool_servers = PoolLocation.objects.find_latest_pool_servers_info_for_date(
                date=calculation_date,
                pool=pool_name
            )

            """
                Unknown pool => pool where individual miners have mined the block / the actual pool name was not provided by the API 
                Unrecognized pool => pool name is provided by the API, but we don't have any data about it in the Excel sheet
                Cloudflare pool => don't know where the pool is located, so use an average emission coefficient of where cloudflare servers are located
            """ 
            def pool_is_unrecognized(pool_servers: QuerySet[PoolLocation]):
                return pool_servers.count() == 0

            if pool_is_unrecognized(pool_servers):
                electricity_consumption_for_server = \
                    cls.get_electricity_usage(
                        average_gear_efficiency_j_gh=average_gear_efficiency_j_gh,
                        pool_hash_rate_eh_s=pool_hash_rate_eh_s,
                        pool_servers_number=1
                    )

                electricity_consumption_kwh_day[UNKNOWN_POOL_LOCATION] += electricity_consumption_for_server
                
                co2_emissions_for_server = \
                    cls.get_co2_emissions(
                            electricity_consumption_for_server=electricity_consumption_for_server,
                            emissions_factor=PoolLocation.objects.find_latest_info_about_unknown_pools(
                                date=calculation_date
                            ).emission_factor
                        )
                co2_emissions_tco2e_day[UNKNOWN_POOL_LOCATION] += co2_emissions_for_server

                logger.info(f"No info about pool {pool_name}; adding {pool_hash_rate_eh_s} to unrecognized sources")
                unrecognized_servers_hash_rate += pool_hash_rate_eh_s

                server_granural_information[UNRECOGNIZED_POOL][0]['co2_emissions'] += co2_emissions_for_server
                server_granural_information[UNRECOGNIZED_POOL][0]['electricity'] += electricity_consumption_for_server

            pool_object = Pool.objects.filter(pool_name=pool_name)

            for pool_server in pool_servers:

                if server_granural_information.get(pool_name) is None:
                    server_granural_information[pool_name] = []

                def get_server_location_name(pool_server):
                    return pool_server.blockchain_pool_location.location_name

                def get_server_location(pool_server):
                    return pool_server.blockchain_pool_location

                server_location = get_server_location_name(pool_server)

                if pool_name == UNKNOWN_POOL:
                    unknown_servers_hash_rate += pool_hash_rate_eh_s
                else:
                    location_obj = get_server_location(pool_server)
                    HashRatePerPoolServer.objects.create(
                        blockchain_pool=pool_object[0],
                        blockchain_pool_location=location_obj,
                        hash_rate=pool_hash_rate_eh_s / pool_servers.count(),
                        date=calculation_date
                    )
                    logger.info(f"Saved hash rate information for pool {pool_name} servers "
                                f"at {server_location} on {calculation_date}: "
                                f"{pool_hash_rate_eh_s / pool_servers.count()}")

                if electricity_consumption_kwh_day.get(server_location) is None:
                    electricity_consumption_kwh_day[server_location] = 0
                if co2_emissions_tco2e_day.get(server_location) is None:
                    co2_emissions_tco2e_day[server_location] = 0

                electricity_consumption_for_multiple_servers = \
                    cls.get_electricity_usage(
                        average_gear_efficiency_j_gh=average_gear_efficiency_j_gh,
                        pool_hash_rate_eh_s=pool_hash_rate_eh_s,
                        pool_servers_number=pool_servers.count()
                    )

                electricity_consumption_kwh_day[server_location] += electricity_consumption_for_multiple_servers

                co2_production_for_server = \
                    cls.get_co2_emissions(
                        electricity_consumption_for_server=electricity_consumption_for_multiple_servers,
                        emissions_factor=pool_server.emission_factor
                    )

                co2_emissions_tco2e_day[server_location] += co2_production_for_server
                    
                if pool_name == UNKNOWN_POOL:
                    server_granural_information[pool_name][0]['co2_emissions'] += co2_production_for_server
                    server_granural_information[pool_name][0]['electricity'] += electricity_consumption_for_multiple_servers
                else: 
                    server_granural_information[pool_name].append(
                        {
                            'server_location': server_location,
                            'co2_emissions': co2_production_for_server,
                            'electricity': electricity_consumption_for_multiple_servers
                        }
                    )

        HashRatePerPoolServer.objects.create(
            blockchain_pool=Pool.objects.get(pool_name=UNKNOWN_POOL),
            blockchain_pool_location=Location.objects.get(location_name=UNKNOWN_POOL_LOCATION),
            hash_rate=unknown_servers_hash_rate,
            date=calculation_date
        )
        logger.info(f"Saved hash rate information for unknown servers "
                    f"on {calculation_date}: "
                    f"{unknown_servers_hash_rate}")
        HashRatePerPoolServer.objects.create(
            blockchain_pool=Pool.objects.get(pool_name=UNRECOGNIZED_POOL),
            blockchain_pool_location=Location.objects.get(location_name=UNKNOWN_POOL_LOCATION),
            hash_rate=unrecognized_servers_hash_rate,
            date=calculation_date
        )
        logger.info(f"Saved hash rate information for unrecognized servers "
                    f"on {calculation_date}: "
                    f"{unrecognized_servers_hash_rate}")

        return electricity_consumption_kwh_day, co2_emissions_tco2e_day, server_granural_information

    @classmethod
    def get_electricity_usage(cls, average_gear_efficiency_j_gh, pool_hash_rate_eh_s, pool_servers_number):
        return HOURS_IN_A_DAY * (EXA_H_S_TO_GIGA_H_S_MULTIPLIER * pool_hash_rate_eh_s) * average_gear_efficiency_j_gh / (pool_servers_number * KWH_MULTIPLIER)

    @classmethod
    def get_co2_emissions(cls, electricity_consumption_for_server, emissions_factor):
        return (electricity_consumption_for_server * emissions_factor) / TONNE_MULTIPLIER
