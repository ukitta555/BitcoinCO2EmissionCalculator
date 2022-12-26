from django.db import models
from django.db.models import UniqueConstraint

from src.bitcoin_emissions.models import Pool, Location
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class PoolLocation(UUIDModel):
    blockchain_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    blockchain_pool_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    valid_for_date = models.DateField()
    emission_factor = models.DecimalField(max_digits=15, decimal_places=10)
    information_source = models.CharField(max_length=100)
