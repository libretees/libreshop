import logging
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class Warehouse(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    address = models.OneToOneField('addresses.Address', null=False, blank=False)

    def __str__(self):
        return 'Warehouse %s' % self.name

    def validate_unique(self, *args, **kwargs):
        super(Warehouse, self).validate_unique(*args, **kwargs)

        queryset = self.__class__._default_manager.filter(
            name__iexact=self.name
        )

        if not self._state.adding and self.pk:
            queryset = queryset.exclude(pk=self.pk)

        if queryset.exists():
            raise ValidationError({
                'name': ['Warehouse with this Name already exists',],
            })

    def save(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        self.validate_unique(exclude)
        super(Warehouse, self).save(*args, **kwargs)
