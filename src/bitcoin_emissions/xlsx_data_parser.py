import logging
from datetime import datetime

import django
import openpyxl
from django.db import transaction
from openpyxl import load_workbook

from src.bitcoin_emissions.consts import CLOUDFLARE_LOCATION_DATA, CLOUDFLARE_REGION, CURRENT_POOL_INFO_SHEET_NAME, \
    ANTMINER_DATA_SHEET_NAME

logger = logging.getLogger(__name__)

class ExcelParser:
    @classmethod
    def parse_excel_for_pool_and_location_info(cls, workbook: openpyxl.Workbook):
        from src.bitcoin_emissions.models import Pool, Location, PoolLocation

        with transaction.atomic():
            for sheet in workbook:
                print(f"Working with sheet {sheet.title}")
                for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                    emission_factor, latitude, location_name, longitude, \
                        pool_name, source, validity_date = cls._fetch_data_about_pool(row, sheet)

                    pool, new_pool_was_created = Pool.objects.get_or_create(pool_name=pool_name)
                    if new_pool_was_created:
                        print(f"Added pool {pool_name} to the database")

                    location, new_location_was_created = Location.objects.get_or_create(
                        location_name=location_name,
                        latitude=latitude,
                        longitude=longitude,
                    )
                    if new_location_was_created:
                        print(f"Added location f{location_name} to the database")

                    PoolLocation.objects.create(
                        blockchain_pool=pool,
                        blockchain_pool_location=location,
                        valid_for_date=validity_date,
                        emission_factor=emission_factor,
                        information_source=source
                    )
                    print(f"Added pool server for pool {pool_name} at location {location_name}")
                    print(f"Finished row {row_index} of sheet {sheet.title}")

    @classmethod
    def _fetch_data_about_pool(cls, row, sheet):
        def server_is_hosted_by_cloudflare(location_name):
            return location_name == CLOUDFLARE_REGION

        pool_name, location_name, emission_factor, source, \
            latitude, longitude = row
        if sheet.title == CURRENT_POOL_INFO_SHEET_NAME:
            validity_date = datetime.today()
        else:
            validity_date = datetime.strptime(sheet.title, "%b %d %Y")
        if server_is_hosted_by_cloudflare(location_name):
            location_name, latitude, longitude = CLOUDFLARE_LOCATION_DATA
        return emission_factor, latitude, location_name, longitude, pool_name, source, validity_date

    @classmethod
    def parse_excel_with_mining_gear_data(cls, workbook: openpyxl.Workbook):
        from src.bitcoin_emissions.models import MiningGear

        with transaction.atomic():
            sheet = workbook[ANTMINER_DATA_SHEET_NAME]
            for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
                name, release_date, efficiency = row
                MiningGear.objects.get_or_create(
                    name=name,
                    release_date=release_date,
                    efficiency=efficiency
                )


if __name__ == '__main__':
    django.setup()
    pool_data = load_workbook(filename='../data/Pool_data_final.xlsx')
    ExcelParser.parse_excel_for_pool_and_location_info(workbook=pool_data)
    mining_gear_data = load_workbook(filename='../../data/Antminer Models[90].xlsx')
    ExcelParser.parse_excel_with_mining_gear_data(workbook=mining_gear_data)
