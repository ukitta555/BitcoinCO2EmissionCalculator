from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class Pool(UUIDModel):
    pool_name = models.CharField(max_length=100)
    locations = models.ManyToManyField("Location", through="PoolLocation")