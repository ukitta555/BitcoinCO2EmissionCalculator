from collections import deque
from datetime import datetime
from datetime import date

import pytest

from src.bitcoin_emissions.consts import UNKNOWN_CO2_EMISSIONS_FACTOR, UNKNOWN_POOL_LOCATION
from src.bitcoin_emissions.models import Pool, Location, PoolLocation


@pytest.fixture
def mock_blocks_data():
    return deque([
        {
            "height": 128,
            "difficulty": 12,
            "pool_name": "QueenPool",
            "date": datetime(year=2020, month=1, day=29)
        },
        {
            "height": 127,
            "difficulty": 3,
            "pool_name": "F2Pool",
            "date": datetime(year=2020, month=1, day=5)
        },
        {
            "height": 126,
            "difficulty": 3,
            "pool_name": "QueenPool",
            "date": datetime(year=2020, month=1, day=4)
        },
        {
            "height": 125,
            "difficulty": 2,
            "pool_name": "City17",
            "date": datetime(year=2020, month=1, day=3)
        },
        {
            "height": 124,
            "difficulty": 2,
            "pool_name": "F2Pool",
            "date": datetime(year=2020, month=1, day=2)
        },
        {
            "height": 123,
            "difficulty": 2,
            "pool_name": "F2Pool",
            "date": datetime(year=2020, month=1, day=1)
        },
    ])


@pytest.fixture
def mock_pool_servers():
    f2pool = Pool.objects.create(pool_name="F2Pool")
    queenpool = Pool.objects.create(pool_name="QueenPool")
    city17 = Pool.objects.create(pool_name="City17")
    unknown_pool = Pool.objects.create(pool_name="unknown")

    london = Location.objects.create(location_name="London", longitude=0, latitude=0)
    seattle = Location.objects.create(location_name="Seattle", longitude=1, latitude=1)
    neverland = Location.objects.create(location_name="Neverland", longitude=2, latitude=2)
    unknown_loc = Location.objects.create(location_name=UNKNOWN_POOL_LOCATION, longitude=3, latitude=3)

    # 2018-01-03
    PoolLocation.objects.create(
        blockchain_pool=queenpool,
        blockchain_pool_location=neverland,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=0.33
    )
    PoolLocation.objects.create(
        blockchain_pool=unknown_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    # 2020-01-01
    PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=0.5
    )
    PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=seattle,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=0.4
    )
    PoolLocation.objects.create(
        blockchain_pool=queenpool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=0.5
    )
    PoolLocation.objects.create(
        blockchain_pool=city17,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=0.5
    )
    PoolLocation.objects.create(
        blockchain_pool=unknown_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
    # 2020-01-03
    PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2020, month=1, day=3),
        emission_factor=0.5
    )
    PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=seattle,
        valid_for_date=datetime(year=2020, month=1, day=3),
        emission_factor=0.4
    )
    PoolLocation.objects.create(
        blockchain_pool=unknown_pool,
        blockchain_pool_location=unknown_loc,
        valid_for_date=datetime(year=2020, month=1, day=3),
        emission_factor=UNKNOWN_CO2_EMISSIONS_FACTOR
    )
