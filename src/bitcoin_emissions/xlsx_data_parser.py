import logging
from datetime import datetime

import openpyxl
from django.db import transaction
from src.bitcoin_emissions.models import MiningGear
from src.bitcoin_emissions.models import Pool, Location, PoolLocation
from django.core import exceptions

from src.bitcoin_emissions.consts import CLOUDFLARE_LOCATION_DATA, CLOUDFLARE_REGION, \
    ANTMINER_DATA_SHEET_NAME

logger = logging.getLogger(__name__)


class ExcelParser:
    @classmethod
    def parse_excel_for_pool_and_location_info(cls, workbook: openpyxl.Workbook):
        with transaction.atomic():
            for sheet in workbook:
                logger.info(f"Working with sheet {sheet.title}")
                for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
                    emission_factor, latitude, location_name, longitude, \
                        pool_name, source, validity_date = cls._fetch_data_about_pool(row, sheet)

                    if not pool_name or (type(pool_name) is str and pool_name.isspace()):
                        continue

                    pool, new_pool_was_created = Pool.objects.get_or_create(pool_name=pool_name)
                    if new_pool_was_created:
                        logger.info(f"Added pool {pool_name} to the database")

                    try: 
                        location = Location.objects.get(
                            location_name=location_name
                        )
                    except Location.DoesNotExist:
                        location = Location.objects.create(
                            location_name = location_name,
                            latitude=latitude,
                            longitude=longitude,
                        )
                        logger.info(f"Added location {location_name} to the database")

                    PoolLocation.objects.create(
                        blockchain_pool=pool,
                        blockchain_pool_location=location,
                        valid_for_date=validity_date,
                        emission_factor=emission_factor,
                        information_source=source
                    )
                    logger.info(f"Added pool server for pool {pool_name} at location {location_name}")
                    logger.info(f"Finished row {row_index} of sheet {sheet.title}")

    @classmethod
    def _fetch_data_about_pool(cls, row, sheet):
        def server_is_hosted_by_cloudflare(location_name):
            return location_name == CLOUDFLARE_REGION

        pool_name, location_name, emission_factor, source, \
            latitude, longitude = row
        validity_date = datetime.strptime(sheet.title, "%b %d %Y")
        if server_is_hosted_by_cloudflare(location_name):
            location_name, latitude, longitude = CLOUDFLARE_LOCATION_DATA
        return emission_factor, latitude, location_name, longitude, pool_name, source, validity_date

    @classmethod
    def parse_excel_with_mining_gear_data(cls, workbook: openpyxl.Workbook):
        with transaction.atomic():
            sheet = workbook[ANTMINER_DATA_SHEET_NAME]
            for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True)):
                name, release_date, efficiency = row
                if not name or (type(name) is str and name.isspace()):
                    continue
                if type(release_date) == str:
                    release_date = datetime.strptime(release_date, "%Y-%m-%d")
                MiningGear.objects.get_or_create(
                    name=name,
                    release_date=release_date,
                    efficiency=efficiency
                )
