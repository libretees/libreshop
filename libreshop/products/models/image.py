import logging
from django.db import models
from model_utils.models import TimeStampedModel
from versatileimagefield.fields import PPOIField, VersatileImageField

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Image(TimeStampedModel):
    product = models.ForeignKey('products.Product', null=False, blank=False)
    title = models.CharField(max_length=2048, null=True, blank=True)
    description = models.CharField(max_length=2048, null=True, blank=True)
    featured = models.BooleanField(default=False)
    file = VersatileImageField(
        upload_to='images/product', max_length=255, null=False, blank=False,
        ppoi_field='image_ppoi' # Image Primary Point of Interest (PPOI)
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.title if self.title else self.file.url
