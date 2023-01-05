from collections import deque
from datetime import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.models import MiningGear, Pool, Location, PoolLocation


@pytest.fixture
def mock_blocks_data():
    return deque([
        {
            "height": 123,
            "difficulty": 2,
            "pool_name": "F2Pool",
        },
        {
            "height": 124,
            "difficulty": 2,
            "pool_name": "F2Pool",
        },
        {
            "height": 125,
            "difficulty": 2,
            "pool_name": "City17",
        },
        {
            "height": 126,
            "difficulty": 3,
            "pool_name": "QueenPool",
        },
        {
            "height": 127,
            "difficulty": 3,
            "pool_name": "F2Pool",
        },
        {
            "height": 128,
            "difficulty": 12,
            "pool_name": "QueenPool",
        },
    ])


@pytest.fixture
def mock_hash_rate_data():
    return {
        "F2Pool": Decimal(10),  # 24 * X * Y = 24 * 10 * 3 = 720; 720 / 1 = 720 GWh
        "QueenPool": Decimal(5),  # 24 * X * Y = 24 * 5 * 3 = 360; 360 / 2 = 180 GWh
        "City17": Decimal(3),  # 24 * X * Y = 24 * 3 * 3 =  216; 216 / 1 = 216 GWh
    }


@pytest.fixture
def mock_mining_gear_data():
    MiningGear.objects.create(
        name="gear0",
        release_date=datetime(year=2019, month=12, day=30),
        efficiency=Decimal(1)
    )
    MiningGear.objects.create(
        name="gear1",
        release_date=datetime(year=2020, month=1, day=1),
        efficiency=Decimal(2)
    )
    MiningGear.objects.create(
        name="gear2",
        release_date=datetime(year=2020, month=1, day=1),
        efficiency=Decimal(3)
    )
    MiningGear.objects.create(
        name="gear3",
        release_date=datetime(year=2020, month=1, day=5),
        efficiency=Decimal(4)
    )
    MiningGear.objects.create(
        name="gear4",
        release_date=datetime(year=2020, month=2, day=1),
        efficiency=Decimal(5)
    )
    MiningGear.objects.create(
        name="gear5",
        release_date=datetime(year=2020, month=3, day=1),
        efficiency=Decimal(6)
    )


@pytest.fixture
def mock_pool_servers():
    f2pool = Pool.objects.create(pool_name="F2Pool")
    queenpool = Pool.objects.create(pool_name="QueenPool")
    city17 = Pool.objects.create(pool_name="City17")

    london = Location.objects.create(location_name="London", longitude=0, latitude=0)
    seattle = Location.objects.create(location_name="Seattle", longitude=1, latitude=1)
    neverland = Location.objects.create(location_name="Neverland", longitude=2, latitude=2)

    PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=0.1
    )
    PoolLocation.objects.create(
        blockchain_pool=f2pool,
        blockchain_pool_location=seattle,
        valid_for_date=datetime(year=2020, month=1, day=3),
        emission_factor=0.2
    )
    PoolLocation.objects.create(
        blockchain_pool=queenpool,
        blockchain_pool_location=neverland,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=0.3
    )
    PoolLocation.objects.create(
        blockchain_pool=queenpool,
        blockchain_pool_location=neverland,
        valid_for_date=datetime(year=2018, month=1, day=3),
        emission_factor=0.3
    )
    PoolLocation.objects.create(
        blockchain_pool=city17,
        blockchain_pool_location=london,
        valid_for_date=datetime(year=2020, month=1, day=1),
        emission_factor=0.1
    )

