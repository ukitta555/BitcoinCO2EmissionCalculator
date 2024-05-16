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
            mock_pool_servers,
    ):
        _, result_2021_01_01, _ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=1)
        )

        for key, val in result_2021_01_01.items():
            result_2021_01_01[key] = result_2021_01_01[key].quantize(Decimal("0.000001"))

        assert result_2021_01_01 == {
            "London": Decimal(((240 + 240 + 144) * 1000000 * 0.5) / 1000).quantize(Decimal("0.000001")),
            "Cloudflare": Decimal(((240 + 0 + 0) * 1000000 * 0.4) / 1000).quantize(Decimal("0.000001")),
            UNKNOWN_POOL_LOCATION:
                Decimal(((48 + 24) * 1000000 * UNKNOWN_CO2_EMISSIONS_FACTOR) / 1000)
                .quantize(Decimal("0.000001"))
        }

    def test_co2_emissions_calculations_not_all_info(
            self,
            mock_hash_rate_data,
            mock_pool_servers,
    ):
        _, result_2021_01_06, _ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=6)
        )

        for key, val in result_2021_01_06.items():
            result_2021_01_06[key] = result_2021_01_06[key].quantize(Decimal("0.000001"))

        assert result_2021_01_06 == {
            "London": Decimal(((360 + 0 + 0) * 1000000 * 0.5) / 1000).quantize(Decimal("0.000001")),
            "Cloudflare": Decimal(((360 + 0 + 0) * 1000000 * 0.4) / 1000).quantize(Decimal("0.000001")),
            UNKNOWN_POOL_LOCATION:
                Decimal(((360 + 216 + 72 + 36) * 1000000 * 1) / 1000)
                .quantize(Decimal("0.000001"))
        }