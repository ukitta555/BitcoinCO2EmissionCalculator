import json
from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from src.bitcoin_emissions.consts import UNKNOWN_POOL, UNKNOWN_POOL_LOCATION, UNRECOGNIZED_POOL


pytestmark = pytest.mark.django_db

class TestHistoryPerPoolView:
    
    def test_history_per_pool_endpoint(
        self,
        mock_history,
        avg_gear_efficiency,
    ):
        api_response = APIClient().get(
            path=reverse('get_metrics_per_pool'),
            data={
                'start': '2021-01-01',
                'end': '2021-01-01'
            },
            format='json'
        )

        pythonized_response = json.loads(api_response.content)
        for idx in range(len(pythonized_response)):
            pythonized_response[idx]["servers_at_locations"] = sorted(pythonized_response[idx]["servers_at_locations"], key = lambda x: x['location_name']) 

        pythonized_response = sorted(pythonized_response, key = lambda x: x['blockchain_pool_name'])


        expected_answer = [
            {
                "date": "2021-01-01",
                "electricity_usage": 0.0,
                "co2e_emissions": 1.0,
                "blockchain_pool_name": "City17",
                "servers_at_locations": [
                    {
                        "longitude": 0.0,
                        "latitude": 0.0,
                        "location_name": "London",
                        "electricity_usage": "0.000000",
                        "co2e_emissions": "1.000000",
                        "is_cloudflare": False,
                    }
                ]
            },
            {
                "date": "2021-01-01",
                "blockchain_pool_name": "F2Pool",
                "electricity_usage": 3.5,
                "co2e_emissions": 4.5,
                "servers_at_locations": [
                        {
                            "longitude": 1.0,
                            "latitude": 1.0,
                            "location_name": "Cloudflare",
                            "electricity_usage": "3.000000",
                            "co2e_emissions": "4.000000",
                            "is_cloudflare": True,
                        },
                        {
                            "longitude": 0.0,
                            "latitude": 0.0,
                            "location_name": "London",
                            "electricity_usage": "0.500000",
                            "co2e_emissions": "0.500000",
                            "is_cloudflare": False,
                        }
                ]
            },
            {
                "date": "2021-01-01",
                "blockchain_pool_name": UNRECOGNIZED_POOL,
                "electricity_usage": 2.5,
                "co2e_emissions": 3.0,
                "servers_at_locations": [
                    {
                        "longitude": 3.0,
                        "latitude": 3.0,
                        "location_name": UNKNOWN_POOL_LOCATION,
                        "electricity_usage": "2.500000",
                        "co2e_emissions": "3.000000",
                        "is_cloudflare": False,
                    }
                ]
            },
            {
                "date": "2021-01-01",
                "blockchain_pool_name": "QueenPool",
                "electricity_usage": 0.5,
                "co2e_emissions": 0.5,
                "servers_at_locations": [
                    {
                        "longitude": 0.0,
                        "latitude": 0.0,
                        "location_name": "London",
                        "electricity_usage": "0.500000",
                        "co2e_emissions": "0.500000",
                        "is_cloudflare": False,
                    }
                ]
            },
            {
                "date": "2021-01-01",
                "electricity_usage": 2.5,
                "co2e_emissions": 3.0,
                "blockchain_pool_name": UNKNOWN_POOL,
                "servers_at_locations": [
                    {
                        "longitude": 3,
                        "latitude": 3,
                        "location_name": UNKNOWN_POOL_LOCATION,
                        "electricity_usage": "2.500000",
                        "co2e_emissions": "3.000000",
                        "is_cloudflare": False,
                    }
                ]
            },
        ]
        assert pythonized_response == expected_answer