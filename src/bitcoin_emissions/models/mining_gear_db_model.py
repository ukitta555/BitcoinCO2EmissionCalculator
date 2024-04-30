from django.db import models
from numpy import mean

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class MiningGearManager(models.Manager):

    def find_average_gear_efficiency_for_date(self, date):
        return mean(
            list(
                map(
                    lambda x: x.efficiency,
                    self.filter(release_date__lte=date)
                    .order_by("-release_date")[:3] # asssuming the database always has at least 3 entries for every date
                )
            )
        )


class MiningGear(UUIDModel):
    name = models.CharField(max_length=150)
    release_date = models.DateField()
    efficiency = models.DecimalField(max_digits=12, decimal_places=11)
    objects = MiningGearManager()

    def __str__(self):
        return f"Gear: {self.name}, release date: {self.release_date}"
