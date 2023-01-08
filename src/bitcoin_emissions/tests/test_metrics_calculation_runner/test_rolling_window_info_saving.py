from datetime import datetime

import pytest
from django.db.models import F

from src.bitcoin_emissions.calculations.metrics_calculation_runner import MetricsCalculationRunner
from src.bitcoin_emissions.models import BlocksFoundByPoolPerWindow

pytestmark = pytest.mark.django_db


class TestRollingWindowInfoSaving:

    def test_rolling_window_info_saving(
            self,
            mock_blocks_data,
            mock_pool_servers,
            correct_rolling_window_info
    ):
        MetricsCalculationRunner._save_info_about_rolling_window(
            rolling_window=mock_blocks_data,
            end_date=datetime(year=2020, month=1, day=29),
        )
        queryset = list(
            BlocksFoundByPoolPerWindow.objects.all()
            .values(
                'window_start_date',
                'window_end_date',
                'blocks_found',
                pool=F('blockchain_pool__pool_name'),
            )
        )
        assert all(mined_blocks_info in queryset for mined_blocks_info in correct_rolling_window_info)
        assert "Randompool" not in queryset


