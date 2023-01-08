from datetime import datetime

import pytest
from django.db.models import F

from src.bitcoin_emissions.calculations.metrics_calculation_runner import MetricsCalculationRunner
from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory

pytestmark = pytest.mark.django_db


class TestCO2AndElectricitySaving:

    def test_co2_and_electricity_saving(
            self,
            mock_pool_servers,
            mock_co2_info,
            mock_electricity_info,
            correct_co2_electricity_data
    ):
        MetricsCalculationRunner._save_info_about_co2_and_electricity(
            date=datetime(year=2020, month=1, day=1),
            co2_data=mock_co2_info,
            electricity_data=mock_electricity_info,
        )
        co2_electricity_data_queryset = \
            PoolElectricityConsumptionAndCO2EEmissionHistory\
            .objects\
            .all()\
            .values(
                "co2e_emissions",
                "electricity_usage",
                "date",
                servers_location=F("location_of_servers__location_name"),
            )
        assert len(co2_electricity_data_queryset) == len(correct_co2_electricity_data)
        assert all([correct_entry in co2_electricity_data_queryset for correct_entry in correct_co2_electricity_data])
