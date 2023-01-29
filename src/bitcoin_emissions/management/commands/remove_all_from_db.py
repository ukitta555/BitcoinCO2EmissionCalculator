from django.core.management import BaseCommand

from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory, HashRatePerPoolServer, \
    AverageEfficiency, NetworkHashRate, BlocksFoundByPoolPerWindow, PoolLocation, Location, Pool, BitcoinDifficulty, \
    MiningGear
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel
from src.bitcoin_emissions.views import logger


class Command(BaseCommand):
    def handle(self, **options):
        PoolElectricityConsumptionAndCO2EEmissionHistory.objects.all().delete()
        logger.info("Removed all history")
        HashRatePerPoolServer.objects.all().delete()
        logger.info("Removed hash rate per server info")
        AverageEfficiency.objects.all().delete()
        logger.info("Removed average efficiency info")
        NetworkHashRate.objects.all().delete()
        logger.info("Removed network hash rate info")
        BlocksFoundByPoolPerWindow.objects.all().delete()
        logger.info("Removed all window info")
        PoolLocation.objects.all().delete()
        logger.info("Removed pool location window info")
        Location.objects.all().delete()
        logger.info("Removed location  info")
        Pool.objects.all().delete()
        logger.info("Removed pool info")
        BitcoinDifficulty.objects.all().delete()
        logger.info("Removed bitcoin difficulty info")
        MiningGear.objects.all().delete()
        logger.info("Removed mining gear info")
        UUIDModel.objects.all().delete()
        logger.info("Removed UUID info")