from django.db import models
from django.db.models import UniqueConstraint

from src.bitcoin_emissions.consts import UNRECOGNIZED_POOL
from src.bitcoin_emissions.models import Pool, Location
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class PoolLocationManager(models.Manager):

    def find_latest_pool_servers_info_for_date(self, date, pool):
        closest_date = self \
            .filter(valid_for_date__lte=date) \
            .order_by("-valid_for_date")[0].valid_for_date

        return self.filter(
            blockchain_pool__pool_name=pool,
            valid_for_date=closest_date
        )
    
    def find_latest_info_about_unknown_pools(self, date) -> "PoolLocation":
        closest_date = self \
            .filter(valid_for_date__lte=date) \
            .order_by("-valid_for_date")[0].valid_for_date
        return self.filter(
            blockchain_pool__pool_name=UNRECOGNIZED_POOL,
            valid_for_date=closest_date
        )[0]

class PoolLocation(UUIDModel):
    class Meta:
        verbose_name_plural = "Servers (Location + Pool combinations)"
        indexes = [
            models.Index(fields=['blockchain_pool_location']),
        ]


    blockchain_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    blockchain_pool_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    valid_for_date = models.DateField()
    emission_factor = models.DecimalField(max_digits=15, decimal_places=10)
    information_source = models.CharField(max_length=100)
    objects = PoolLocationManager()

    def __str__(self):
        return f"Server: valid for {self.valid_for_date}, pool {self.blockchain_pool.pool_name}, location {self.blockchain_pool_location.location_name}"