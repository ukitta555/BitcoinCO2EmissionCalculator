from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class BitcoinDifficulty(UUIDModel):
    class Meta:
        verbose_name_plural = "Bitcoin mining difficulty"

    date = models.DateField()
    difficulty = models.DecimalField(max_digits=50, decimal_places=6)

    def __str__(self):
        return f"Bitcoin difficulty for date {self.date}: {self.difficulty}"