import logging
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class Communication(TimeStampedModel):
    order = models.ForeignKey('Order', null=True, blank=True)
    from_email = models.EmailField(null=False, blank=False)
    to_email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=998, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
