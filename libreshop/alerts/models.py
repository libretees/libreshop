import logging
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Alert(TimeStampedModel):
    title = models.CharField(
        max_length=64, unique=True, null=False, blank=False
    )
    description = models.CharField(max_length=2048, null=False, blank=False)
    expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
