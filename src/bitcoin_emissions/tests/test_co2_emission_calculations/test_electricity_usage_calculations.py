from datetime import datetime
from decimal import Decimal

import pytest

from src.bitcoin_emissions.calculations.electicity_and_co2_usage_calculator import ElectricityAndCO2Calculator

pytestmark = pytest.mark.django_db


class TestElectricityUsageCalculations:

    def test_electricity_usage_calc(
            self,
            mock_hash_rate_data,
            mock_mining_gear_data,
            mock_pool_servers,
    ):
        result_2020_01_01, _ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2020, month=1, day=1),
        )
        result_2020_01_06, _ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2020, month=1, day=6),
        )

        assert result_2020_01_01 == {
            "London": Decimal(240 + 240 + 144).quantize(Decimal("0.00000000001")), # F2 + Queen + City17
            "Seattle": Decimal(240).quantize(Decimal("0.00000000001")), # F2
            "unknown": Decimal(48 + 24).quantize(Decimal("0.00000000001")) # unknown + PoolWithoutInfo
        }
        assert result_2020_01_06 == {
            "London": Decimal(360).quantize(Decimal("0.00000000001")), # F2
            "Seattle": Decimal(360).quantize(Decimal("0.00000000001")),
            # Queen + City17 + unknown + PoolWithoutInfo
            "unknown": Decimal(360 + 216 + 72 + 36).quantize(Decimal("0.00000000001"))
        }
