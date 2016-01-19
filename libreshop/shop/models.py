import logging
from django.db import models
from model_utils.models import TimeStampedModel
from jsonfield import JSONField

logger = logging.getLogger(__name__)


class Category(TimeStampedModel):

    class Meta():
        verbose_name_plural = 'categories'

    parent_category = models.ForeignKey('self',
                                        null=True,
                                        blank=True)
    name = models.CharField(max_length=32,
                            null=False,
                            blank=False,
                            unique=True)
    slug = models.SlugField(max_length=32,
                            null=True,
                            blank=True,
                            db_index=True)
    products = models.ManyToManyField('products.Product',
                                      blank=True)

    def __str__(self):
          return self.name
