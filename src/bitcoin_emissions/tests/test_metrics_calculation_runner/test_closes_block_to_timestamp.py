from datetime import datetime

import pytz

from src.bitcoin_emissions.calculations.metrics_calculation_runner import BeforeOrAfter, MetricsCalculationRunner


class TestClosestBlock:
    def test_closest_block_to_timestamp(self):
        date = datetime(year=2021, month=1, day=1, tzinfo=pytz.UTC)
        result = MetricsCalculationRunner._get_closest_block_to_date(date=date, before_or_after=BeforeOrAfter.AFTER)
        assert result == 663913
        result = MetricsCalculationRunner._get_closest_block_to_date(date=date, before_or_after=BeforeOrAfter.BEFORE)
        assert result == 663912