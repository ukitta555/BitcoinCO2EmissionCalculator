from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class BitcoinDifficulty(UUIDModel):
    date = models.DateField()
    difficulty = models.DecimalField(max_digits=50, decimal_places=6)

