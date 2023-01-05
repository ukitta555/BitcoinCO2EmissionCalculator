from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class MiningGear(UUIDModel):
    name = models.CharField(max_length=150)
    release_date = models.DateField()
    efficiency = models.DecimalField(max_digits=12, decimal_places=11)

    def __str__(self):
        return f"Gear: {self.name}, release date: {self.release_date}"
