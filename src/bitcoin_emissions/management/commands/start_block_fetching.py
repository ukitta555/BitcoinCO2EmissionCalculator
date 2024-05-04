import datetime
import logging

from django.core.management.base import BaseCommand

from src.bitcoin_emissions.calculations.metrics_calculation_runner import MetricsCalculationRunner
from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory, HashRatePerPoolServer, \
    AverageEfficiency, NetworkHashRate, BlocksFoundByPoolPerWindow, BitcoinDifficulty
from src.bitcoin_emissions.models.co2_electricity_history_per_server_db_model import CO2ElectricityHistoryPerServer

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--fetch_for_last_24h', action='store_true')

    def handle(self, fetch_for_last_24h, **options):
        end_date = None
        if fetch_for_last_24h:
            start_date = datetime.datetime.today() - datetime.timedelta(days=1)
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date
            logger.info(end_date)
        else:
            start_date = datetime.datetime(year=2021, month=1, day=1)
        logger.info(f"For date {start_date}: ")
        PoolElectricityConsumptionAndCO2EEmissionHistory.objects.filter(date=start_date).delete()
        logger.info("Removed location history info")
        CO2ElectricityHistoryPerServer.objects.filter(date=start_date).delete()
        logger.info("Removed pool history info")
        HashRatePerPoolServer.objects.filter(date=start_date).delete()
        logger.info("Removed hash rate per server info")
        AverageEfficiency.objects.filter(date=start_date).delete()
        logger.info("Removed average efficiency info")
        NetworkHashRate.objects.filter(date=start_date).delete()
        logger.info("Removed network hash rate info")
        BlocksFoundByPoolPerWindow.objects.filter(window_start_date=start_date).delete()
        logger.info("Removed block window info")
        BitcoinDifficulty.objects.filter(date=start_date).delete()
        logger.info("Removed bitcoin difficulty info")

        MetricsCalculationRunner.calculate_metrics_for_date_range(
            start_date=start_date,
            end_date=end_date
        )