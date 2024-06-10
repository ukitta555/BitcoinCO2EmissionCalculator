from django.db import models

from src.bitcoin_emissions.models import Location
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class ElectricityConsumptionAndCO2EEmissionHistoryManager(models.Manager):

    def get_history_for_range(self, start_date, end_date):
        return self.filter(
            date__gte=start_date,
            date__lte=end_date
        ).select_related(
            'location_of_servers'
        )


class PoolElectricityConsumptionAndCO2EEmissionHistory(UUIDModel):
    class Meta:
        verbose_name_plural = "Emissions history per location"
        indexes = [
            models.Index(fields=['date']),
        ]


    date = models.DateField()
    electricity_usage = models.DecimalField(max_digits=24, decimal_places=6)
    co2e_emissions = models.DecimalField(max_digits=24, decimal_places=6)
    location_of_servers = models.ForeignKey(Location, on_delete=models.CASCADE)
    objects = ElectricityConsumptionAndCO2EEmissionHistoryManager()

    def __str__(self) -> str:
        return f"Location emissions history: {self.date}, {self.location_of_servers.location_name}"