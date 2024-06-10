from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class Location(UUIDModel):
    class Meta:
        indexes = [
            models.Index(fields=['location_name']),
        ]

    location_name = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"Location {self.location_name}"
