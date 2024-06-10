from django.db import models

from src.bitcoin_emissions.models import Location, Pool


class HashRatePerPoolServer(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['date', 'blockchain_pool_location']),
        ]

    blockchain_pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    blockchain_pool_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    hash_rate = models.DecimalField(max_digits=100, decimal_places=12)
    date = models.DateField()
