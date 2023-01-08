from datetime import datetime
from decimal import Decimal

import pandas as pd
import pytest

from src.bitcoin_emissions.calculations.helper_calculators.hashrate_calculator import HashRateCalculator

pytestmark = pytest.mark.django_db

class TestPoolHashrateCalculations:

    def test_average_difficulty_per_window(self, mock_blocks_data):
        result = HashRateCalculator.get_averaged_difficulty(
            rolling_window_df=pd.DataFrame(mock_blocks_data),
            date=datetime(year=1, month=1, day=1)  # mock, we don't care
        )
        assert result == 4

    def test_pool_hash_rate_calculations(self, mock_blocks_data):
        result = HashRateCalculator.calculate_hash_rates_per_pool(
            rolling_window=mock_blocks_data,
            date=datetime(year=1, month=1, day=1)  # mock, we don't care
        )
        for key, val in result.items():
            result[key] = result[key].quantize(Decimal("0.0000001"))

        assert result.get("F2Pool") == Decimal(2**32/(10**18 * 300)).quantize(Decimal("0.0000001"))
        assert result.get("QueenPool") == Decimal(2**32/(10**18 * 600)).quantize(Decimal("0.0000001"))
        assert result.get("City17") == Decimal(2**32/(10**18 * 900)).quantize(Decimal("0.0000001"))

