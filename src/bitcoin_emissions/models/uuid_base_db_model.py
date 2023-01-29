import uuid
from django.db import models


class UUIDModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)