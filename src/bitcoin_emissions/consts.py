from datetime import datetime
from decimal import Decimal

CLOUDFLARE_REGION = "Region Unknown"
CLOUDFLARE_LOCATION_DATA = [
    "Cloudflare",  # location name
    39.274589,  # latitude
    -37.762002,  # longitude
]
CURRENT_POOL_INFO_SHEET_NAME = "Current information"
ANTMINER_DATA_SHEET_NAME = "Antminer Models"
GENESIS_BLOCK_DATE = datetime(year=2009, month=1, day=3)
AVERAGE_BLOCK_MINING_TIME_SECS = 600
GIGA_MULTIPLIER = 10 ** 18
HOURS_IN_A_DAY = 24
TONNE_MULTIPLIER = 1000

UNKNOWN_POOL_LATITUDE = Decimal(40.527483)
UNKNOWN_POOL_LONGITUDE = Decimal(-38.193144)
UNKNOWN_CO2_EMISSIONS_FACTOR = Decimal(0.442)

