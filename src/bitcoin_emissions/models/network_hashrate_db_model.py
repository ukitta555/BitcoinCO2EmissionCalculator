from django.db import models

from src.bitcoin_emissions.models.uuid_base_db_model import UUIDModel


class NetworkHashRate(UUIDModel):
    class Meta:
        verbose_name_plural = "Network hash rate"

    date = models.DateField()
    network_hash_rate_eh_s = models.DecimalField(max_digits=100, decimal_places=12)

    def __str__(self):
        return f"Network hashrate for date {self.date}: {self.network_hash_rate_eh_s} EH/s"