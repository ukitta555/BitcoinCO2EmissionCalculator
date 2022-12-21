from django.db import models
from src.bitcoin_emissions.models import PoolLocation
from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class CO2EmissionFactor(UUIDModel):
    pool_location = models.ForeignKey(PoolLocation, on_delete=models.CASCADE)
    date = models.DateField()
    co2_emission_factor = models.DecimalField(max_digits=15, decimal_places=6)
    information_source = models.CharField(max_length=100)  # for manual cross-checking of the data validity
