from datetime import datetime

import pytest

from src.bitcoin_emissions.calculations.helper_calculators.electicity_and_co2_usage_calculator import \
    ElectricityAndCO2Calculator
from src.bitcoin_emissions.models import HashRatePerPoolServer, AverageEfficiency

pytestmark = pytest.mark.django_db


class TestIntermediateInfoSaving:

    def test_avg_gear_efficiency_save_to_db(
            self,
            mock_hash_rate_data,
            mock_pool_servers,
    ):
        result_2021_01_01, _, __ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=1),
        )
        result_2021_01_06, _, __ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=6),
        )
        avg_gear_efficiency_2021_01_01 = AverageEfficiency.objects.get(
            date=datetime(year=2021, month=1, day=1)
        )
        avg_gear_efficiency_2021_01_06 = AverageEfficiency.objects.get(
            date=datetime(year=2021, month=1, day=6)
        )

        assert avg_gear_efficiency_2021_01_01.average_efficiency_j_gh == 2
        assert avg_gear_efficiency_2021_01_06.average_efficiency_j_gh == 3

    def test_server_hash_rate_save_to_db(
            self,
            mock_hash_rate_data,
            correct_server_hash_rate_objects,
    ):
        result_2021_01_01, _, __ = ElectricityAndCO2Calculator.calculate(
            pool_hash_rates=mock_hash_rate_data,
            calculation_date=datetime(year=2021, month=1, day=1),
        )

        server_hash_rate_info = \
            HashRatePerPoolServer.objects \
                .all() \
                .values(
                "blockchain_pool",
                "blockchain_pool_location",
                "hash_rate",
                "date"
            )

        # assert server_hash_rate_info == correct_server_hash_rate_objects
        assert len(server_hash_rate_info) == len(correct_server_hash_rate_objects)
        assert all([obj in correct_server_hash_rate_objects for obj in server_hash_rate_info])

