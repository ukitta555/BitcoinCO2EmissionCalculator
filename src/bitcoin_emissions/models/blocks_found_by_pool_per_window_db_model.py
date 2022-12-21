from django.db import models

from src.bitcoin_emissions.models import Pool
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class BlocksFoundByPoolPerWindow(UUIDModel):
    blocks_found = models.IntegerField()
    window_start_date = models.DateField()
    window_end_date = models.DateField()
    blockchain_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)