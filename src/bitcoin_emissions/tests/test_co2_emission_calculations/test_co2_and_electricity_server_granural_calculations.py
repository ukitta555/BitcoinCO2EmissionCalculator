from datetime import datetime
from decimal import ROUND_DOWN, Decimal, getcontext
import pprint

import pytest

from src.bitcoin_emissions.calculations.helper_calculators.electicity_and_co2_usage_calculator import \
    ElectricityAndCO2Calculator
from src.bitcoin_emissions.consts import GIGA_MULTIPLIER, UNKNOWN_CO2_EMISSIONS_FACTOR, UNKNOWN_POOL, UNKNOWN_POOL_LOCATION, UNRECOGNIZED_POOL

pytestmark = pytest.mark.django_db


# TODO: remove quantize calls or think about how to get around those...
class TestCO2AndElectricityGranural:

    def test_granural(
            self,
            mock_hash_rate_data,
            mock_pool_servers,
    ):
        _, __, result_2021_01_01 = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=1),
        )
        _, __, result_2021_01_06 = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=6),
        )
        pprint.pprint(result_2021_01_01)
        assert result_2021_01_01 == {
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
        pprint.pprint(result_2021_01_06)
        getcontext().prec = 45
        assert result_2021_01_06 == {
            "F2Pool": [
                {
                    "server_location": "London",
                    "co2_emissions": Decimal((360 * GIGA_MULTIPLIER * 0.5) / 1000).quantize(Decimal("0.00000000001")),
                    "electricity": Decimal(360 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001")),
                },
                {
                    "server_location": "Cloudflare",
                    "co2_emissions": Decimal((360 * GIGA_MULTIPLIER * 0.4) / 1000).quantize(Decimal("0.00000000001")),
                    "electricity": Decimal(360 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001")),
                }
            ],
            UNKNOWN_POOL: [
                {
                    "server_location": UNKNOWN_POOL_LOCATION,
                    "co2_emissions": Decimal((72 * GIGA_MULTIPLIER * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000).quantize(Decimal("0.00000000001")),
                    "electricity": Decimal(72 * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001"))
                }
            ],
            UNRECOGNIZED_POOL: [
                {
                    "server_location": UNKNOWN_POOL_LOCATION,
                    "co2_emissions": Decimal(((360 + 216 + 36) * GIGA_MULTIPLIER * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000).quantize(Decimal("0.0000000000000000000001"), rounding=ROUND_DOWN),
                    "electricity": Decimal((360 + 216 + 36) * GIGA_MULTIPLIER).quantize(Decimal("0.00000000001")),
                },
            ],
        }