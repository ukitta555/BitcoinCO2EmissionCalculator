from decimal import Decimal, ROUND_DOWN

import pandas as pd

from src.bitcoin_emissions.calculations.hashrate_calculator import HashRateCalculator

class TestPoolHashrateCalculations:

    def test_average_difficulty_per_window(self, mock_blocks_data):
        result = HashRateCalculator.get_averaged_difficulty(
            rolling_window_df=pd.DataFrame(mock_blocks_data)
        )
        assert result == 4

    def test_pool_hash_rate_calculations(self, mock_blocks_data):
        result = HashRateCalculator.calculate_hash_rates_per_pool(
            rolling_window=mock_blocks_data
        )

        assert result.get("F2Pool") == Decimal(2**32/(10**18 * 300)).quantize(Decimal('.0000001'))
        assert result.get("QueenPool") == Decimal(2**32/(10**18 * 600)).quantize(Decimal('.0000001'))
        assert result.get("City17") == Decimal(2**32/(10**18 * 900)).quantize(Decimal('.0000001'))

