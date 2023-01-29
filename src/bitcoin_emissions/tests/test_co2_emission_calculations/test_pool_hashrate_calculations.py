import datetime
from decimal import Decimal

import pandas as pd
import pytest

from src.bitcoin_emissions.calculations.helper_calculators.hashrate_calculator import HashRateCalculator
from src.bitcoin_emissions.consts import AVERAGE_BLOCK_MINING_TIME_SECS, EXA_MULTIPLIER
from src.bitcoin_emissions.models import NetworkHashRate

pytestmark = pytest.mark.django_db

class TestPoolHashrateCalculations:

    def test_average_difficulty_per_window(self, mock_blocks_data):
        result = HashRateCalculator.get_averaged_difficulty(
            rolling_window_df=pd.DataFrame(mock_blocks_data),
            date=datetime.datetime(year=1, month=1, day=1)  # mock, we don't care
        )
        assert result == 4

    def test_pool_hash_rate_calculations(self, mock_blocks_data):
        mock_date = datetime.datetime(year=1, month=1, day=1)
        result = HashRateCalculator.calculate_hash_rates_per_pool(
            rolling_window=mock_blocks_data,
            date=mock_date
        )
        for key, val in result.items():
            result[key] = result[key].quantize(Decimal("0.0000001"))

        assert result.get("F2Pool") == Decimal(2**32/(10**18 * 300)).quantize(Decimal("0.0000001"))
        assert result.get("QueenPool") == Decimal(2**32/(10**18 * 600)).quantize(Decimal("0.0000001"))
        assert result.get("City17") == Decimal(2**32/(10**18 * 900)).quantize(Decimal("0.0000001"))

        # TODO: separate test for this; no need for it to be here
        network_hash_rate = NetworkHashRate.objects.get(date=datetime.datetime(year=1, month=1, day=1))
        avg_difficulty = 4

        assert {
                "date": network_hash_rate.date,
                "network_hash_rate_eh_s": network_hash_rate.network_hash_rate_eh_s.quantize(Decimal("0.000000001"))
            } == {
                "date": datetime.date(year=1, month=1, day=1),
                "network_hash_rate_eh_s": Decimal((avg_difficulty * 2 ** 32) / (AVERAGE_BLOCK_MINING_TIME_SECS *
                                                                     EXA_MULTIPLIER)).quantize(Decimal("0.000000001")),
            }