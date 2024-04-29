import json
from collections import OrderedDict
from rest_framework.test import APIClient
import pytest
from django.urls import reverse

from src.bitcoin_emissions.consts import UNKNOWN_POOL_LOCATION, UNKNOWN_POOL, UNRECOGNIZED_POOL

pytestmark = pytest.mark.django_db

class TestHistoryPerLocationView:

    def test_history_endpoint(
            self,
            mock_history,
            avg_gear_efficiency,
    ):
        api_response = APIClient().get(
            path=reverse('get_metrics'),
            data={
                'start': '2021-01-01',
                'end': '2021-01-01'
            },
            format='json'
        )
        assert json.loads(api_response.content) == [
            {
                "co2e_emissions": 2.0,
                "date": '2021-01-01',
                "electricity_usage": 1.0,
                "location_of_servers": {
                    "longitude": "0.000000",
                    "latitude": "0.000000",
                    "location_name": "London",
                },
                "servers_at_location": [
                    {
                        "blockchain_pool_name": "F2Pool",
                        "hash_rate": 5.0,
                        "co2e_emissions": 0.5,
                        "electricity_usage": 0.5,
                    },
                    {
                        "blockchain_pool_name": "QueenPool",
                        "hash_rate": 5.0,
                        "co2e_emissions": 0.5,
                        "electricity_usage": 0.5,
                    },
                    {
                        "blockchain_pool_name": "City17",
                        "hash_rate": 3.0,
                        "co2e_emissions": 1,
                        "electricity_usage": 0,
                    },
                ],
                "is_cloudflare": False,
                "averaged_gear_efficiency": 2.0,
                "network_hash_rate_720_block_window": 100.5,
                "averaged_difficulty": 4.0,
            },
            {
                "co2e_emissions": 4.0,
                "date": '2021-01-01',
                "electricity_usage": 3.0,
                "location_of_servers": {
                        "longitude": "1.000000",
                        "latitude": "1.000000",
                        "location_name": "Cloudflare"
                },
                "servers_at_location": [
                    {
                        "blockchain_pool_name": "F2Pool",
                        "hash_rate": 5.0,
                        "co2e_emissions": 4.0,
                        "electricity_usage": 3.0,
                    }
                ],
                "is_cloudflare": True,
                "averaged_gear_efficiency": 2.0,
                "network_hash_rate_720_block_window": 100.5,
                "averaged_difficulty": 4.0,
            },
            {
                "co2e_emissions": 6.0,
                "date": '2021-01-01',
                "electricity_usage": 5.0,
                "location_of_servers": {
                    "longitude": "3.000000",
                    "latitude": "3.000000",
                    "location_name": UNKNOWN_POOL_LOCATION,
                },
                "servers_at_location": [
                    {
                        "blockchain_pool_name": UNKNOWN_POOL,
                        "hash_rate": 1.0,
                        "co2e_emissions": 3,
                        "electricity_usage": 2.5,
                    },
                    {
                        "blockchain_pool_name": UNRECOGNIZED_POOL,
                        "hash_rate": 1.0,
                        "co2e_emissions": 3,
                        "electricity_usage": 2.5,
                    },
                ],
                "is_cloudflare": False,
                "averaged_gear_efficiency": 2.0,
                "network_hash_rate_720_block_window": 100.5,
                "averaged_difficulty": 4.0,
            },
        ]
