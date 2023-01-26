from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class AverageEfficiency(UUIDModel):

    date = models.DateField()
    average_efficiency_j_gh = models.DecimalField(max_digits=100, decimal_places=12)
