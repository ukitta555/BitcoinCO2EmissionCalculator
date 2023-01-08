from datetime import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.models import MiningGear, Pool, Location, PoolLocation


@pytest.fixture
def mock_hash_rate_data():
    # comments are for the 2020-01-06 case; 10**6 multiplier is omitted
    return {
        "F2Pool": Decimal(10),  # 24 * X * Y = 24 * 10 * 3 = 720; 720 / 1 = 720 GWh
        "QueenPool": Decimal(5),  # 24 * X * Y = 24 * 5 * 3 = 360; 360 / 1 = 360 GWh (unknown)
        "City17": Decimal(3),  # 24 * X * Y = 24 * 3 * 3 =  216; 216 / 1 = 216 GWh (unknown)
        "unknown": Decimal(1), # 24 * X * Y = 24 * 1 * 3 = 72; 216 / 1 = 72 GWh (unknown)
        "PoolWithoutInfo": Decimal(0.5), # 24 * X * Y = 24 * 0.5 * 3 =  36; 216 / 1 = 36 GWh (unknown)
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
