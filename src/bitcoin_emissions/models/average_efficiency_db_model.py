from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class AverageEfficiency(UUIDModel):
    class Meta:
        verbose_name_plural = "Average gear efficiency"


    date = models.DateField()
    average_efficiency_j_gh = models.DecimalField(max_digits=100, decimal_places=12)

    def __str__(self):
        return f"Average gear efficiency for date {self.date}: {self.average_efficiency_j_gh} j/gh"