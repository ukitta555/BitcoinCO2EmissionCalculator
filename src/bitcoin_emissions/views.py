import logging
from datetime import datetime

from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from src.bitcoin_emissions.calculations.metrics_calculation_runner import MetricsCalculationRunner
from src.bitcoin_emissions.management.commands.parse_excel_data import Command as ParseExcelCommand
from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory, Pool, Location, PoolLocation, \
    BitcoinDifficulty, MiningGear, BlocksFoundByPoolPerWindow, AverageEfficiency, HashRatePerPoolServer, NetworkHashRate
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel
from src.bitcoin_emissions.serializers import EmissionSerializer

logger = logging.getLogger(__name__)

"""
DONE 1. The pool name (this one is relevant for the front end) - foreign key join with removing duplicate tuples 
(pool, location) to preserve since we only care about location (?)
2. Whether the server is cloudflare - boolean flag by location
3. The average difficulty - create table, query by date 
4. Average efficiency of mining equipment that were used to calculate the network hashrate - create table, 
query by date
5. The network hashrate - create table, query by date 
DONE 6. The pool hashrate related to each entry ie. at the level of each server on each date - 
attach to each foreign key the hashrate value for tuple (pool, location)
"""


class Co2AndElectricityView(APIView):

    def get(self, request):
        try:
            start_date = datetime.strptime(request.GET.get('start', '2021-01-01'), '%Y-%m-%d')
            end_date = datetime.strptime(request.GET.get('end', '2021-01-01'), '%Y-%m-%d')
            if not datetime(year=2021, month=1, day=1) <= start_date <= end_date <= datetime.today():
                raise Exception
        except Exception as e:
            return HttpResponseBadRequest(
                content="Bad request, please check "
                        "whether you provided dates in a correct "
                        "format (YYYY-MM-DD)"
            )
        try:
            result = \
                PoolElectricityConsumptionAndCO2EEmissionHistory\
                .objects\
                .get_history_for_range(
                    start_date=start_date,
                    end_date=end_date
                )

            serializer = EmissionSerializer(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest(content="Request failed while fetching the data.")


class StartFetchingView(APIView):

    def get(self, request):
        MetricsCalculationRunner.calculate_metrics_up_until_today(
            start_date=datetime(year=2021, month=1, day=1)
        )
        return Response(data="Data fetching completed successfully!", status=200)


class ImportPoolData(APIView):

    def get(self, request):
        ParseExcelCommand().handle()
        return Response(data="Pool data import completed successfully!", status=200)


class CleanAllTables(APIView):

    def get(self, request):
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
        return Response(data="Data cleanup completed successfully!", status=200)


