import logging
from django.db import models
from django.db.models.expressions import Case, When, Value
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class AlertManager(models.Manager):
    def get_queryset(self):
        queryset = super(AlertManager, self).get_queryset()
        queryset = queryset.annotate(
            active=Case(
                When(expiration__lte=timezone.now(), then=Value(False)),
                default=Value(True),
                output_field=models.BooleanField()
            )
        )
        return queryset


class Alert(TimeStampedModel):
    title = models.CharField(
        max_length=64, unique=True, null=False, blank=False
    )
    description = models.CharField(max_length=2048, null=False, blank=False)
    expiration = models.DateTimeField(null=True, blank=True)

    objects = AlertManager()

    def __str__(self):
        return self.title
