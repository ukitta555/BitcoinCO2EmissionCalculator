from datetime import datetime

from django.http import HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from src.bitcoin_emissions.models import PoolElectricityConsumptionAndCO2EEmissionHistory
from src.bitcoin_emissions.serializers import EmissionSerializer


class Co2AndElectricityView(APIView):

    def get(self, request):
        try:
            start_date = datetime.strptime(request.GET.get('start', '2021-01-01'), '%Y-%m-%d')
            end_date = datetime.strptime(request.GET.get('end', '2021-01-01'), '%Y-%m-%d')
            if not datetime(year=2021, month=1, day=1) <= start_date <= end_date <= datetime.today():
                raise Exception
        except Exception as e:
            return HttpResponseBadRequest(content="Bad request, please check whether you provided dates in a correct "
                                                  "format (YYYY-MM-DD)")
        try:
            result = \
                PoolElectricityConsumptionAndCO2EEmissionHistory\
                .objects\
                .filter(
                    date__gte=start_date,
                    date__lte=end_date
                ).select_related(
                    'location_of_servers'
                )
            serializer = EmissionSerializer(result, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return HttpResponseBadRequest(content="Request failed while fetching the data.")



