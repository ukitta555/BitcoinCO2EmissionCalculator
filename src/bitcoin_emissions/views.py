import logging
from datetime import datetime

from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory
from src.bitcoin_emissions.models import CO2ElectricityHistoryPerServer
from src.bitcoin_emissions.serializers import EmissionSerializer, EmissionSerializerPerPool, EmissionSerializerShort

logger = logging.getLogger(__name__)


class Co2AndElectricityPerPoolView(APIView):
    
    # TODO: think whether we should limit the dates for which we fetch data
    # so that we can avoid querying the thing with too large of a request (most likely yes)
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
            # TODO: fill in the logic for the pool view
            result = CO2ElectricityHistoryPerServer\
                .objects\
                .get_history_for_range_with_unique_date_and_pool_name(
                    start_date=start_date,
                    end_date=end_date
                )
            serializer = EmissionSerializerPerPool(result, many = True)
            return Response(serializer.data)
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest(content="Request failed while fetching the data.")


class Co2AndElectricityPerLocationView(APIView):

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
            # logger.info(start_date, end_date)
            serializer = EmissionSerializerShort(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.exception(e)
            return HttpResponseBadRequest(content="Request failed while fetching the data.")



