from collections import deque
from datetime import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.consts import CLOUDFLARE_LOCATION_DATA, UNKNOWN_CO2_EMISSIONS_FACTOR, UNKNOWN_POOL_LOCATION, UNKNOWN_POOL, \
    UNRECOGNIZED_POOL
from src.bitcoin_emissions.models import Pool, Location, PoolLocation, HashRatePerPoolServer, \
    PoolElectricityConsumptionAndCO2EEmissionHistory, MiningGear, NetworkHashRate, BitcoinDifficulty, AverageEfficiency
from src.bitcoin_emissions.models.co2_electricity_history_per_server_db_model import CO2ElectricityHistoryPerServer


@pytest.fixture
def mock_blocks_data():
    return deque([
        {
            "height": 128,
            "difficulty": 12,
            "pool_name": "QueenPool",
            "date": datetime(year=2021, month=1, day=29)
        },
        {
            "height": 127,
            "difficulty": 3,
            "pool_name": "F2Pool",
            "date": datetime(year=2021, month=1, day=5)
        },
        {
            "height": 126,
            "difficulty": 3,
            "pool_name": "QueenPool",
            "date": datetime(year=2021, month=1, day=4)
        },
        {
            "height": 125,
            "difficulty": 2,
            "pool_name": "City17",
            "date": datetime(year=2021, month=1, day=3)
        },
        {
            "height": 124,
            "difficulty": 2,
            "pool_name": "F2Pool",
            "date": datetime(year=2021, month=1, day=2)
        },
        {
            "height": 123,
            "difficulty": 2,
            "pool_name": "F2Pool",
            "date": datetime(year=2021, month=1, day=1)
        },
    ])

@pytest.fixture
def avg_gear_efficiency():
    AverageEfficiency.objects.create(
        date=datetime(year=2021, month=1, day=1),
        average_efficiency_j_gh=Decimal(2)
    )

@pytest.fixture
def avg_btc_difficulty():
    BitcoinDifficulty.objects.create(
        date=datetime(year=2021, month=1, day=1),
        difficulty=Decimal(4),
    )

@pytest.fixture
def network_hash_rate():
    NetworkHashRate.objects.create(
        date=datetime(year=2021, month=1, day=1),
        network_hash_rate_eh_s=Decimal(100.5)
    )

@pytest.fixture
def mock_mining_gear_data():
    MiningGear.objects.create(
        name="gear0",
        release_date=datetime(year=2019, month=12, day=30),
        efficiency=Decimal(1)
    )
    MiningGear.objects.create(
        name="gear1",
        release_date=datetime(year=2021, month=1, day=1),
        efficiency=Decimal(2)
    )
    MiningGear.objects.create(
        name="gear2",
        release_date=datetime(year=2021, month=1, day=1),
        efficiency=Decimal(3)
    )
    MiningGear.objects.create(
        name="gear3",
        release_date=datetime(year=2021, month=1, day=5),
        efficiency=Decimal(4)
    )
    MiningGear.objects.create(
        name="gear4",
        release_date=datetime(year=2021, month=2, day=1),
        efficiency=Decimal(5)
    )
    MiningGear.objects.create(
        name="gear5",
        release_date=datetime(year=2021, month=3, day=1),
        efficiency=Decimal(6)
    )


@pytest.fixture
def mock_pool_servers(
    mock_mining_gear_data,
    network_hash_rate,
    avg_btc_difficulty,
):
    f2pool = Pool.objects.create(pool_name="F2Pool")
    queenpool = Pool.objects.create(pool_name="QueenPool")
    city17 = Pool.objects.create(pool_name="City17")
    unknown_pool = Pool.objects.create(pool_name=UNKNOWN_POOL)
    unrecognized_pool = Pool.objects.create(pool_name=UNRECOGNIZED_POOL)

    london = Location.objects.create(location_name="London", longitude=0, latitude=0)
    cloudflare = Location.objects.create(location_name=CLOUDFLARE_LOCATION_DATA[0], longitude=1, latitude=1)
    neverland = Location.objects.create(location_name="Neverland", longitude=2, latitude=2)
    unknown_loc = Location.objects.create(location_name=UNKNOWN_POOL_LOCATION, longitude=3, latitude=3)

    # 2018-01-03
    queenpool_neverland_2018_01_03 = PoolLocation.objects.create(
        blockchain_pool=queenpool,
        blockchain_pool_location=neverland,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=0.33
    )
    unknown_2018_01_03 = PoolLocation.objects.create(
        blockchain_pool=unknown_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    unrecognized_2018_01_03 = PoolLocation.objects.create(
        blockchain_pool=unrecognized_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    # 2021-01-01
    f2pool_london_2021_01_01 = PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2021, month=1, day=1),
        emission_factor=0.5
    )
    f2pool_seattle_2021_01_01 = PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=cloudflare,
        valid_for_date=datetime(year=2021, month=1, day=1),
        emission_factor=0.4
    )
    queenpool_london_2021_01_01 = PoolLocation.objects.create(
        blockchain_pool=queenpool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2021, month=1, day=1),
        emission_factor=0.5
    )
    city17_london_2021_01_01 = PoolLocation.objects.create(
        blockchain_pool=city17,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2021, month=1, day=1),
        emission_factor=0.5
    )
    unknown_2021_01_01 = PoolLocation.objects.create(
        blockchain_pool=unknown_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2021, month=1, day=1),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    unrecognized_2021_01_01 = PoolLocation.objects.create(
        blockchain_pool=unrecognized_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2021, month=1, day=1),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    # 2021-01-03
    f2pool_london_2021_01_03 = PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2021, month=1, day=3),
        emission_factor=0.5
    )
    f2pool_seattle_2021_01_03 = PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=cloudflare,
        valid_for_date=datetime(year=2021, month=1, day=3),
        emission_factor=0.4
    )
    unknown_2021_01_03 = PoolLocation.objects.create(
        blockchain_pool=unknown_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2021, month=1, day=3),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    unrecognized_2021_01_03 = PoolLocation.objects.create(
        blockchain_pool=unrecognized_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2021, month=1, day=3),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    return {
        "pools": {
            "F2Pool": f2pool,
            "QueenPool": queenpool,
            "City17": city17,
            UNKNOWN_POOL: unknown_pool,
            UNRECOGNIZED_POOL: unrecognized_pool,
        },
        "locations": {
            "London": london,
            "Cloudflare": cloudflare,
            "Neverland": neverland,
            "unknown_loc": unknown_loc,
        },
        "pool_locations": {
            "queenpool_neverland_2018_01_03": queenpool_neverland_2018_01_03,
            "unknown_2018_01_03": unknown_2018_01_03,
            "unrecognized_2018_01_03": unrecognized_2018_01_03,
            "f2pool_london_2021_01_01": f2pool_london_2021_01_01,
            "f2pool_seattle_2021_01_01": f2pool_seattle_2021_01_01,
            "queenpool_london_2021_01_01": queenpool_london_2021_01_01,
            "city17_london_2021_01_01": city17_london_2021_01_01,
            "unknown_2021_01_01": unknown_2021_01_01,
            "unrecognized_2021_01_01": unrecognized_2021_01_01,
            "f2pool_london_2021_01_03": f2pool_london_2021_01_03,
            "f2pool_seattle_2021_01_03": f2pool_seattle_2021_01_03,
            "unknown_2021_01_03": unknown_2021_01_03,
            "unrecognized_2021_01_03": unrecognized_2021_01_03
        }
    }

@pytest.fixture
def mock_history(mock_pool_servers):
    mock_hash_rates = [
        5,  # queenpool_neverland_2018_01_03,
        1,  # unknown_2018_01_03,
        1,  # unrecognized_2018_01_03,
        5,  # f2pool_london_2021_01_01
        5,  # f2pool_seattle_2021_01_01
        5,  # queenpool_london_2021_01_01
        3,  # city17_london_2021_01_01
        1,  # unknown_2021_01_01,
        1,  # unrecognized_2021_01_01
        5,  # f2pool_london_2021_01_03
        5,  # f2pool_seattle_2021_01_03
        1,  # unknown_2021_01_03
        1,  # unrecognized_2021_01_03
    ]
    for pool_location, mock_hash_rate in \
            zip(mock_pool_servers.get("pool_locations").values(), mock_hash_rates):
        HashRatePerPoolServer.objects.create(
            blockchain_pool=pool_location.blockchain_pool,
            blockchain_pool_location=pool_location.blockchain_pool_location,
            hash_rate=mock_hash_rate,
            date=pool_location.valid_for_date
        )

    PoolElectricityConsumptionAndCO2EEmissionHistory.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=1,
        co2e_emissions=2,
        location_of_servers=mock_pool_servers.get("locations").get("London")
    )
    PoolElectricityConsumptionAndCO2EEmissionHistory.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=3,
        co2e_emissions=4,
        location_of_servers=mock_pool_servers.get("locations").get("Cloudflare")
    )
    PoolElectricityConsumptionAndCO2EEmissionHistory.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=5,
        co2e_emissions=6,
        location_of_servers=mock_pool_servers.get("locations").get("unknown_loc")
    )

    CO2ElectricityHistoryPerServer.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=3,
        co2e_emissions=4,
        server_info=mock_pool_servers.get("pool_locations").get("f2pool_seattle_2021_01_01")
    )
    CO2ElectricityHistoryPerServer.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=0.5,
        co2e_emissions=0.5,
        server_info=mock_pool_servers.get("pool_locations").get("f2pool_london_2021_01_01")
    )
    CO2ElectricityHistoryPerServer.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=0.5,
        co2e_emissions=0.5,
        server_info=mock_pool_servers.get("pool_locations").get("queenpool_london_2021_01_01")
    )
    CO2ElectricityHistoryPerServer.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=0,
        co2e_emissions=1,
        server_info=mock_pool_servers.get("pool_locations").get("city17_london_2021_01_01")
    )
    CO2ElectricityHistoryPerServer.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=2.5,
        co2e_emissions=3,
        server_info=mock_pool_servers.get("pool_locations").get("unknown_2021_01_01")
    )
    CO2ElectricityHistoryPerServer.objects.create(
        date=datetime(year=2021, month=1, day=1),
        electricity_usage=2.5,
        co2e_emissions=3,
        server_info=mock_pool_servers.get("pool_locations").get("unrecognized_2021_01_01")
    )