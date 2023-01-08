from datetime import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.calculations.helper_calculators.electicity_and_co2_usage_calculator import ElectricityAndCO2Calculator
from src.bitcoin_emissions.consts import UNKNOWN_CO2_EMISSIONS_FACTOR, UNKNOWN_POOL_LOCATION

pytestmark = pytest.mark.django_db


class TestCO2EmissionsCalculation:
    def test_co2_emissions_calculations_all_info(
            self,
            mock_hash_rate_data,
            mock_mining_gear_data,
            mock_pool_servers,
    ):
        _, result_2020_01_01 = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2020, month=1, day=1)
        )

        for key, val in result_2020_01_01.items():
            result_2020_01_01[key] = result_2020_01_01[key].quantize(Decimal("0.000001"))

        assert result_2020_01_01 == {
            "London": Decimal(((240 + 240 + 144) * 1000000 * 0.5) / 1000).quantize(Decimal("0.000001")),
            "Seattle": Decimal(((240 + 0 + 0) * 1000000 * 0.4) / 1000).quantize(Decimal("0.000001")),
            UNKNOWN_POOL_LOCATION:
                Decimal(((48 + 24) * 1000000 * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
                .quantize(Decimal("0.000001"))
        }

    def test_co2_emissions_calculations_not_all_info(
            self,
            mock_hash_rate_data,
            mock_mining_gear_data,
            mock_pool_servers,
    ):
        _, result_2020_01_06 = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2020, month=1, day=6)
        )

        for key, val in result_2020_01_06.items():
            result_2020_01_06[key] = result_2020_01_06[key].quantize(Decimal("0.000001"))

        assert result_2020_01_06 == {
            "London": Decimal(((360 + 0 + 0) * 1000000 * 0.5) / 1000).quantize(Decimal("0.000001")),
            "Seattle": Decimal(((360 + 0 + 0) * 1000000 * 0.4) / 1000).quantize(Decimal("0.000001")),
            UNKNOWN_POOL_LOCATION:
                Decimal(((360 + 216 + 72 + 36) * 1000000 * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
                .quantize(Decimal("0.000001"))
        }



# assert result_2020_01_01 == [
#     {
#         "name": "London",
#         "latitude": Decimal(0).quantize(Decimal(".000001")),
#         "longitude": Decimal(0).quantize(Decimal(".000001")),
#         "electricity_usage": Decimal(240 + 240 + 144).quantize(Decimal(".000001")),
#         "CO2_usage": Decimal(((240 + 240 + 144) * 0.5) / 1000).quantize(Decimal(".000001")),
#     },
#     {
#         "name": "Seattle",
#         "latitude": Decimal(1).quantize(Decimal(".000001")),
#         "longitude": Decimal(1).quantize(Decimal(".000001")),
#         "electricity_usage": Decimal(240 + 0 + 0).quantize(Decimal(".000001")),
#         "CO2_usage": Decimal(((240 + 0 + 0) * 0.4) / 1000).quantize(Decimal(".000001")),
#     },
#     {
#         "name": "unknown",
#         "latitude": Decimal(UNKNOWN_POOL_LATITUDE).quantize(Decimal(".000001")),
#         "longitude": Decimal(UNKNOWN_POOL_LONGITUDE).quantize(Decimal(".000001")),
#         "electricity_usage": Decimal(240 + 0 + 0).quantize(Decimal(".000001")),
#         "CO2_usage":
#             Decimal(((48 + 24) * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
#             .quantize(Decimal(".000001")),
#     },
# ]


# assert result_2020_01_06 == [
#     {
#         "name": "London",
#         "latitude": Decimal(0).quantize(Decimal(".000001")),
#         "longitude": Decimal(0).quantize(Decimal(".000001")),
#         "electricity_usage": Decimal(360 + 0 + 0).quantize(Decimal(".000001")),
#         "CO2_usage": Decimal(((360 + 0 + 0) * 0.5) / 1000).quantize(Decimal(".000001")),
#     },
#     {
#         "name": "Seattle",
#         "latitude": Decimal(1).quantize(Decimal(".000001")),
#         "longitude": Decimal(1).quantize(Decimal(".000001")),
#         "electricity_usage": Decimal(360 + 0 + 0).quantize(Decimal(".000001")),
#         "CO2_usage": Decimal(((360 + 0 + 0) * 0.4) / 1000).quantize(Decimal(".000001")),
#     },
#     {
#         "name": "unknown",
#         "latitude": Decimal(UNKNOWN_POOL_LATITUDE).quantize(Decimal(".000001")),
#         "longitude": Decimal(UNKNOWN_POOL_LONGITUDE).quantize(Decimal(".000001")),
#         "electricity_usage": Decimal(360 + 216 + 72 + 36).quantize(Decimal(".000001")),
#         "CO2_usage":
#             Decimal(((360 + 216 + 72 + 36) * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
#             .quantize(Decimal(".000001")),
#     },
# ]
