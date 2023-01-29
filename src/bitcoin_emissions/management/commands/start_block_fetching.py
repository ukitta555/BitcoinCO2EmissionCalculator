from datetime import datetime

from django.core.management.base import BaseCommand

from src.bitcoin_emissions.calculations.metrics_calculation_runner import MetricsCalculationRunner


class Command(BaseCommand):
    def handle(self, **options):
        MetricsCalculationRunner.calculate_metrics_up_until_today(
            start_date=datetime(year=2021, month=1, day=1)
        )