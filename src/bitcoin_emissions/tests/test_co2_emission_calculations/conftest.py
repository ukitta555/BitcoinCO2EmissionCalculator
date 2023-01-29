import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.consts import UNKNOWN_POOL, UNKNOWN_POOL_LOCATION
from src.bitcoin_emissions.models import MiningGear, Pool, Location, PoolLocation


@pytest.fixture
def mock_hash_rate_data():
    # comments are for the 2021-01-06 case; 10**6 multiplier is omitted
    return {
        "F2Pool": Decimal(10),  # 24 * X * Y = 24 * 10 * 3 = 720; 720 / 1 = 720 GWh
        "QueenPool": Decimal(5),  # 24 * X * Y = 24 * 5 * 3 = 360; 360 / 1 = 360 GWh (unknown)
        "City17": Decimal(3),  # 24 * X * Y = 24 * 3 * 3 =  216; 216 / 1 = 216 GWh (unknown)
        "unknown": Decimal(1),  # 24 * X * Y = 24 * 1 * 3 = 72; 216 / 1 = 72 GWh (unknown)
        "PoolWithoutInfo": Decimal(0.5),  # 24 * X * Y = 24 * 0.5 * 3 =  36; 216 / 1 = 36 GWh (unknown)
    }

@pytest.fixture
def correct_server_hash_rate_objects(
        mock_pool_servers
):
    return [
        {
            "blockchain_pool": mock_pool_servers.get("pools").get("F2Pool").uuid,
            "blockchain_pool_location": mock_pool_servers.get("locations").get("London").uuid,
            "hash_rate": Decimal(5.000000000000),
            "date": datetime.date(year=2021, month=1, day=1),
        },
        {
            "blockchain_pool": mock_pool_servers.get("pools").get("QueenPool").uuid,
            "blockchain_pool_location": mock_pool_servers.get("locations").get("London").uuid,
            "hash_rate": Decimal(5.000000000000),
            "date": datetime.date(year=2021, month=1, day=1),
        },
        {
            "blockchain_pool": mock_pool_servers.get("pools").get("City17").uuid,
            "blockchain_pool_location": mock_pool_servers.get("locations").get("London").uuid,
            "hash_rate": Decimal(3.000000000000),
            "date": datetime.date(year=2021, month=1, day=1),
        },
        {
            "blockchain_pool": mock_pool_servers.get("pools").get("F2Pool").uuid,
            "blockchain_pool_location": mock_pool_servers.get("locations").get("Cloudflare").uuid,
            "hash_rate": Decimal(5.000000000000),
            "date": datetime.date(year=2021, month=1, day=1),
        },
        {
            "blockchain_pool": mock_pool_servers.get("pools").get(UNKNOWN_POOL).uuid,
            "blockchain_pool_location": mock_pool_servers.get("locations").get("unknown_loc").uuid,
            "hash_rate": Decimal(1.500000000000),
            "date": datetime.date(year=2021, month=1, day=1),
        },
    ]