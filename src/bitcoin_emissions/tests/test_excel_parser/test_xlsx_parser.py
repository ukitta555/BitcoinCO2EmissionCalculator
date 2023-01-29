import datetime
import os

import pytest
from openpyxl import load_workbook

from src.bitcoin_emissions.models import Pool, Location, PoolLocation
from src.bitcoin_emissions.xlsx_data_parser import ExcelParser

pytestmark = pytest.mark.django_db


class TestExcelParser:

    def test_pool_info_parser(self):
        workbook = load_workbook(os.path.dirname(__file__) + "/mock_pool_data.xlsx")
        ExcelParser().parse_excel_for_pool_and_location_info(workbook=workbook)
        assert self._get_pool_names_from_db() == \
               {
                   "F2Pool",
                   "AntPool",
                   "Poolin",
                   "Binance Pool",
                   "ViaBTC"
               }

        assert self._get_locations_from_db() == \
               {
                   "Cloudflare",
                   "Germany, Hessen, Frankfurt am Main",
                   "Singapore",
                   "United States of America,Washington,Seattle",
                   "San Francisco, California, United States"
               }

        assert self._get_poollocations_of_mocked_pool() == \
               self._correct_mocked_poollocations()
        


    def _correct_mocked_poollocations(self):
        cloudflare_location_uuid = self._get_cloudflare_location_uuid()
        san_francisco_location_uuid = self._get_san_francisco_location_uuid()
        f2pool_uuid = self._get_f2pool_uuid()
        return [
            {
                "blockchain_pool_id": f2pool_uuid,
                "blockchain_pool_location_id": san_francisco_location_uuid,
                "valid_for_date": datetime.date(2022, 3, 1),
                "information_source": "Carbon FootPrint",
                "emission_factor": "0.2055300000",
            },
            {
                "blockchain_pool_id": f2pool_uuid,
                "blockchain_pool_location_id": cloudflare_location_uuid,
                "valid_for_date": datetime.date(2022, 3, 1),
                "information_source": "AnotherSite",
                "emission_factor": "0.5146588640",
            },
            {
                "blockchain_pool_id": f2pool_uuid,
                "blockchain_pool_location_id": cloudflare_location_uuid,
                "valid_for_date": datetime.date(2022, 2, 10),
                "information_source": "N/A",
                "emission_factor": "0.5146588640",
            }
        ]

    def _get_f2pool_uuid(self):
        return Pool.objects.get(pool_name="F2Pool").uuid

    def _get_san_francisco_location_uuid(self):
        return Location.objects.get(location_name="San Francisco, California, "
                                                  "United States").uuid

    def _get_cloudflare_location_uuid(self):
        return Location.objects.get(location_name="Cloudflare").uuid

    def _get_poollocations_of_mocked_pool(self):
        pool_locations = list(PoolLocation.objects.filter(
            blockchain_pool__pool_name="F2Pool"
        ).values(
            "blockchain_pool_id",
            "blockchain_pool_location_id",
            "valid_for_date",
            "information_source",
            "emission_factor"
        ))
        for pl in pool_locations:
            pl["emission_factor"] = str(pl["emission_factor"])
        return pool_locations

    def _get_pool_names_from_db(self):
        return set(map(lambda x: x.get('pool_name'),
                       Pool.objects.all().values('pool_name'))
                   )

    def _get_locations_from_db(self):
        return set(map(lambda x: x.get('location_name'),
                       Location.objects.all().values('location_name'))
                   )