import logging
from decimal import Decimal
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

# Initialize logger.
logger = logging.getLogger(__name__)

class Transaction(TimeStampedModel):
    order = models.ForeignKey('Order', null=True, blank=True)
    transaction_id = models.CharField(
        max_length=8, null=False, blank=False, unique=True, verbose_name='ID'
    )
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False,
        default=Decimal('0.00')
    )
    cardholder_name = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)
    payment_card_type = models.CharField(
        max_length=16, null=True, blank=True, verbose_name='Card Type'
    )
    payment_card_last_4 = models.CharField(
        max_length=8, null=True, blank=True, verbose_name='Last 4'
    )
    payment_card_expiration_date = models.CharField(
        max_length=8, null=True, blank=True, verbose_name='Expiration Date',
        validators=[RegexValidator(
            r'^(0[1-9]|1[0-2])[/-]\d{2}$',
            message='Expiration date must be in MM/YY or MM-YY format',
            code='Invalid expiration date'
        )]
    )
    created_at = models.DateTimeField(default=timezone.now)
    origin_ip_address = models.GenericIPAddressField(null=True, blank=True)
    authorized = models.BooleanField(default=False)

    class Meta:
        get_latest_by = 'created_at'
