from datetime import datetime

import pytest

from src.bitcoin_emissions.models import MiningGear

pytestmark = pytest.mark.django_db


class TestMiningGearAvgEfficiency:

    def test_mining_gear_avg_efficiency(
            self,
            mock_mining_gear_data,
    ):
        result = MiningGear.objects.find_average_gear_efficiency_for_date(
            date=datetime(year=2021, month=1, day=1)
        )
        assert result == 2

