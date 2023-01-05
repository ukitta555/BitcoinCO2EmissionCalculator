from datetime import datetime

import pytest

from src.bitcoin_emissions.calculations.electicity_usage_calculator import ElectricityUsageCalculator

pytestmark = pytest.mark.django_db


class TestElectricityUsageCalculations:

    def test_electricity_usage_calc(
            self,
            mock_hash_rate_data,
            mock_mining_gear_data,
            mock_pool_servers,
    ):
        result_2020_01_01 = ElectricityUsageCalculator.calculate_electricity_usage(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2020, month=1, day=1),
        )
        result_2020_01_06 = ElectricityUsageCalculator.calculate_electricity_usage(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2020, month=1, day=6),
        )

        # assert result_2020_01_01 == {
        #     "F2Pool": 480,
        #     "QueenPool": 120,
        #     "City17": 144,
        # }
        #
        # assert result_2020_01_06 == {
        #     "F2Pool": 720,
        #     "QueenPool": 180,
        #     "City17": 216,
        # }

        assert result_2020_01_01 == {
            "F2Pool": 480,
            "QueenPool": "No data!",
            "City17": 144,
        }
        assert result_2020_01_06 == {
            "F2Pool": 720,
            "QueenPool": "No data!",
            "City17": "No data!",
        }
