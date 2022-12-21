from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class PoolElectricityConsumptionAndCO2EEmissionHistory(UUIDModel):
    date = models.DateField()
    electricity_usage = models.DecimalField(max_digits=24, decimal_places=6)
    co2e_emissions = models.DecimalField(max_digits=24, decimal_places=6)
