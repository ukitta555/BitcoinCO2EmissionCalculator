from collections import deque
from datetime import date
from datetime import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.consts import GIGA_MULTIPLIER, KWH_MULTIPLIER, KWH_TO_GWH_MULTIPLIER, UNKNOWN_POOL, UNKNOWN_CO2_EMISSIONS_FACTOR, UNKNOWN_POOL_LOCATION, UNRECOGNIZED_POOL


@pytest.fixture
def mock_blocks_data():
    return deque([
        {
            "height": 130,
            "difficulty": 12,
            "pool_name": UNKNOWN_POOL,
            "date": datetime(year=2021, month=1, day=29)
        },
        {
            "height": 129,
            "difficulty": 12,
            "pool_name": "QueenPool",
            "date": datetime(year=2021, month=1, day=29)
        },
        {
            "height": 128,
            "difficulty": 3,
            "pool_name": "Randompool",
            "date": datetime(year=2021, month=1, day=6)
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


@pytest.fixture()
def correct_rolling_window_info():
    return [
        {
            'window_start_date': date(year=2021, month=1, day=1),
            'window_end_date': date(year=2021, month=1, day=29),
            'blocks_found': 3,
            'pool': "F2Pool",
        },
        {
            'window_start_date': date(year=2021, month=1, day=1),
            'window_end_date': date(year=2021, month=1, day=29),
            'blocks_found': 2,
            'pool': "QueenPool",
        },
        {
            'window_start_date': date(year=2021, month=1, day=1),
            'window_end_date': date(year=2021, month=1, day=29),
            'blocks_found': 1,
            'pool': "City17",
        },
        {
            'window_start_date': date(year=2021, month=1, day=1),
            'window_end_date': date(year=2021, month=1, day=29),
            'blocks_found': 2,
            'pool': UNKNOWN_POOL,
        }
    ]


@pytest.fixture
def mock_co2_info():
    return {
            "London": Decimal(((240 + 240 + 144) * 1000000 * 0.5) / 1000).quantize(Decimal("0.00000000001")),
            "Cloudflare": Decimal(((240 + 0 + 0) * 1000000 * 0.4) / 1000).quantize(Decimal("0.00000000001")),
            UNKNOWN_POOL_LOCATION:
                Decimal(((48 + 24) * 1000000 * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
                .quantize(Decimal("0.00000000001"))
        }


@pytest.fixture
def mock_electricity_info():
    return {
        "London": Decimal((240 + 240 + 144) * 1000000).quantize(Decimal("0.00000000001")),  # F2 + Queen + City17
        "Cloudflare": Decimal(240 * 1000000).quantize(Decimal("0.00000000001")),  # F2
        UNKNOWN_POOL_LOCATION: Decimal((48 + 24) * 1000000).quantize(Decimal("0.00000000001"))  # unknown + PoolWithoutInfo
    }


@pytest.fixture
def correct_co2_electricity_data():
    return [
        {
            "servers_location": "London",
            "date": date(year=2021, month=1, day=1),
            "electricity_usage": Decimal(240 + 240 + 144).quantize(Decimal("0.00000000001")),
            "co2e_emissions": Decimal(((240 + 240 + 144) * 1000000 * 0.5) / 1000).quantize(Decimal("0.00000000001")),
        },
        {
            "servers_location": "Cloudflare",
            "date": date(year=2021, month=1, day=1),
            "electricity_usage": Decimal(240 + 0 + 0).quantize(Decimal("0.00000000001")),
            "co2e_emissions": Decimal(((240 + 0 + 0) * 1000000 * 0.4) / 1000).quantize(Decimal("0.00000000001")),
        },
        {
            "servers_location": UNKNOWN_POOL_LOCATION,
            "date": date(year=2021, month=1, day=1),
            "electricity_usage": Decimal(48 + 24).quantize(Decimal("0.00000000001")),
            "co2e_emissions":
                Decimal(((48 + 24) * 1000000 * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
                .quantize(Decimal("0.00000000001")),
        },
    ]


@pytest.fixture
def mock_granural_data():
    return {
        "F2Pool": [
            {
                "server_location": "London",
                "co2_emissions": Decimal((240 * GIGA_MULTIPLIER * 0.5) / 1000).quantize(Decimal("0.00000000001")),
                "electricity": Decimal(240 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001")),
            },
            {
                "server_location": "Cloudflare",
                "co2_emissions": Decimal((240 * GIGA_MULTIPLIER * 0.4) / 1000).quantize(Decimal("0.00000000001")),
                "electricity": Decimal(240 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001")),
            }
        ],
        "QueenPool": [
            {
                "server_location": "London",
                "co2_emissions": Decimal((240 * GIGA_MULTIPLIER * 0.5) / 1000).quantize(Decimal("0.00000000001")),
                "electricity": Decimal(240 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001"))
            }
        ],
        "City17": [
            {
                "server_location": "London",
                "co2_emissions": Decimal((144 * GIGA_MULTIPLIER * 0.5) / 1000).quantize(Decimal("0.00000000001")),
                "electricity": Decimal(144 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001"))
            }
        ],
        UNKNOWN_POOL: [
            {
                "server_location": UNKNOWN_POOL_LOCATION,
                "co2_emissions": Decimal((48 * GIGA_MULTIPLIER * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000).quantize(Decimal("0.00000000001")),
                "electricity": Decimal(48 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001"))
            }
        ],
        UNRECOGNIZED_POOL: [
            {
                "server_location": UNKNOWN_POOL_LOCATION,
                "co2_emissions": Decimal((24 * GIGA_MULTIPLIER * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000).quantize(Decimal("0.00000000000000000000001")),
                "electricity": Decimal(24 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001"))
            }
        ],
    }

#     date = models.DateField()
#     electricity_usage = models.DecimalField(max_digits=24, decimal_places=6)
#     co2e_emissions = models.DecimalField(max_digits=24, decimal_places=6)
#     server_info = models.ForeignKey(PoolLocation, on_delete=models.CASCADE)
#     objects = CO2ElectricityHistoryPerServerManager()

@pytest.fixture
def correct_granural_data():
    return [
        {
            "_server_info": "F2Pool",
            "date": date(year=2021, month=1, day=1),
            "co2e_emissions": Decimal((240 * GIGA_MULTIPLIER * 0.5) / 1000),
            "electricity_usage": Decimal(240 * GIGA_MULTIPLIER) / KWH_TO_GWH_MULTIPLIER,
        },
        {
            "_server_info": "F2Pool",
            "date": date(year=2021, month=1, day=1),
            "co2e_emissions": Decimal((240 * GIGA_MULTIPLIER * 0.4) / 1000),
            "electricity_usage": Decimal(240 * GIGA_MULTIPLIER) / KWH_TO_GWH_MULTIPLIER,
        },
        {
            "_server_info": "QueenPool",
            "date": date(year=2021, month=1, day=1),
            "co2e_emissions": Decimal((240 * GIGA_MULTIPLIER * 0.5) / 1000),
            "electricity_usage": Decimal(240 * GIGA_MULTIPLIER) / KWH_TO_GWH_MULTIPLIER
        },
        {
            "_server_info": "City17",
            "date": date(year=2021, month=1, day=1),
            "co2e_emissions": Decimal((144 * GIGA_MULTIPLIER * 0.5) / 1000),
            "electricity_usage": Decimal(144 * GIGA_MULTIPLIER) / KWH_TO_GWH_MULTIPLIER
        },
        {
            "_server_info": UNRECOGNIZED_POOL,
            "date": date(year=2021, month=1, day=1),
            "co2e_emissions": Decimal((24 * GIGA_MULTIPLIER * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000).quantize(Decimal("0.00000000001")),
            "electricity_usage": Decimal(24 * GIGA_MULTIPLIER) / KWH_TO_GWH_MULTIPLIER
        },
        {
            "_server_info": UNKNOWN_POOL,
            "date": date(year=2021, month=1, day=1),
            "co2e_emissions": Decimal((48 * GIGA_MULTIPLIER * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000).quantize(Decimal("0.00000000001")),
            "electricity_usage": Decimal(48 * GIGA_MULTIPLIER) / KWH_TO_GWH_MULTIPLIER
        },
    ]
