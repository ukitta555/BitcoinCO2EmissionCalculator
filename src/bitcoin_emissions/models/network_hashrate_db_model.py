from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class NetworkHashRate(UUIDModel):

    date = models.DateField()
    network_hash_rate_eh_s = models.DecimalField(max_digits=100, decimal_places=12)
