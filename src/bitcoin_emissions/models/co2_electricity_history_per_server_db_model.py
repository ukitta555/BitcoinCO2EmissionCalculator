from django.db import models

from src.bitcoin_emissions.models.pool_locations_db_model import PoolLocation
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class CO2ElectricityHistoryPerServerManager(models.Manager):

    def get_history_for_range(self, start_date, end_date):
        return self.filter(
            date__gte=start_date,
            date__lte=end_date
        ).select_related(
            'server_info'
        )
    
    def get_history_for_range_with_unique_date_and_pool_name(self, start_date, end_date):
        return self.filter(
            date__gte=start_date,
            date__lte=end_date
        ).select_related(
            'server_info'
        ).distinct(
            'date',
            'server_info__blockchain_pool'
        )


class CO2ElectricityHistoryPerServer(UUIDModel):
    class Meta:
        verbose_name_plural = "Emissions history per pool"

    date = models.DateField()
    electricity_usage = models.DecimalField(max_digits=24, decimal_places=6)
    co2e_emissions = models.DecimalField(max_digits=24, decimal_places=6)
    server_info = models.ForeignKey(PoolLocation, on_delete=models.CASCADE)
    objects = CO2ElectricityHistoryPerServerManager()

    def __str__(self) -> str:
        return f"Server emissions history: {self.date}, {self.server_info.blockchain_pool}"
