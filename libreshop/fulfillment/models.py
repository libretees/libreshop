import importlib
import logging
from decimal import Decimal
from random import randrange
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.mail import EmailMessage
from django.db import models
from django.template import Context, Engine
from django.utils import timezone
from model_utils.models import TimeStampedModel
from orders.models import Communication
from django_measurement.models import MeasurementField
from measurement.measures import Weight

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your models here.
class Supplier(TimeStampedModel):

    name = models.CharField(max_length=64, unique=True, null=False, blank=False)
    fulfillment_backend = models.CharField(
        max_length=128, null=False, blank=False
    )
    fulfillment_time = models.TimeField(null=True, blank=True)


    def load_fulfillment_backend(self):

        backend = self.fulfillment_backend
        index = backend.rfind('.')
        module_name, attribute_name = backend[:index], backend[index+1:]
        module, attribute = None, None
        try:
            module = importlib.import_module(module_name)
            attribute = getattr(module, attribute_name)
        except ImportError as e:
            logger.critical('Unable to import module \'%s\'.' % module_name)
        except AttributeError as e:
            logger.critical('\'%s\' module has no attribute \'%s\'.' %
                (module_name, attribute_name))

        return attribute


    def __str__(self):
        return self.name


class FulfillmentSetting(TimeStampedModel):

    class Meta:
        unique_together = ('supplier', 'name')

    supplier = models.ForeignKey('Supplier', null=False, blank=False)
    name = models.CharField(max_length=64, unique=True, null=False, blank=False)

    def __str__(self):
        return '%s: %s' % (self.supplier.name, self.name)


class FulfillmentSettingValue(TimeStampedModel):

    class Meta:
        unique_together = (
            ('setting', 'product'), ('setting', 'variant')
        )

    setting = models.ForeignKey(
        'FulfillmentSetting', null=True, blank=True
    )
    product = models.ForeignKey('products.Product', null=True, blank=True)
    variant = models.ForeignKey('products.Variant', null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)


class FulfillmentOrder(TimeStampedModel):
    order_id = models.CharField(
        max_length=32, null=False, blank=False, unique=True, verbose_name='ID'
    )
    subtotal = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    shipping_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    tax = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    fees = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    total = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    created_at = models.DateTimeField(
        default=timezone.now, null=False, blank=False
    )


class FulfillmentPurchase(TimeStampedModel):

    order = models.ForeignKey('FulfillmentOrder', null=False, blank=False)
    purchase = models.ForeignKey('orders.Purchase', null=False, blank=False)

    subtotal = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    shipping_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    tax = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    fees = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    total = models.DecimalField(
        max_digits=8, decimal_places=2, null=False, blank=False,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )


class Carrier(TimeStampedModel):
    name = models.CharField(
        max_length=32, null=False, blank=False, unique=True
    )
    unit_of_measure = models.CharField(verbose_name='Preferred Unit of Measure',
        max_length=2, choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('oz', 'oz'),
            ('lb', 'lb')))

    def __str__(self):
        return self.name


def get_token(token=None):
    generate = lambda: '{:08x}'.format(randrange(2**32))
    if not token:
        token = generate()
    while Shipment.objects.filter(token=token):
        token = generate()
    return token



class ShipmentManager(models.Manager):

    def create(self, *args, **kwargs):
        token = kwargs.pop('token', None)
        kwargs.update({
            'token': get_token(token=token)
        })
        return super(ShipmentManager, self).create(*args, **kwargs)


class Shipment(TimeStampedModel):

    template_name = 'fulfillment/shipment_confirmation.html'

    order = models.ForeignKey('orders.Order', null=False, blank=False)
    token = models.CharField(max_length=8, null=False, blank=False, unique=True,
        default=get_token)
    carrier = models.ForeignKey('Carrier', null=False, blank=False)
    tracking_id = models.CharField(
        max_length=64, null=False, blank=False, unique=True,
        verbose_name='Tracking ID'
    )
    shipping_cost = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        default=Decimal('0.00'), validators=[
            MinValueValidator(Decimal('0.00'))
        ]
    )
    weight = MeasurementField(
        measurement=Weight, blank=True, null=True,
        unit_choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('oz', 'oz'),
            ('lb', 'lb')
        )
    )

    objects = ShipmentManager()

    def get_email_body(self):
        # Load the default template engine.
        TemplateEngine = Engine.get_default()

        # Render a context to the template specified in `template_name`.
        template = TemplateEngine.get_template(self.template_name)
        context = Context({
            'carrier': self.carrier,
            'order': self.order,
            'tracking_id': self.tracking_id,
            'multiple_shipments': any(
                bool(purchase.variant.suppliers) for purchase
                in self.order.purchases.all()
            ),
            'shipment_date': self.created
        })
        body = template.render(context)

        return body

    def notify_recipient(self):

        email_addresses = {
            communication.to_email for communication
            in self.order.communication_set.all()
        }

        emails_sent = 0
        if email_addresses:
            body = self.get_email_body()
            for email_address in email_addresses:
                subject = (
                    'Your LibreShop Order %s has shipped!' % self.order.token)
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email_address],
                    bcc=[],
                    connection=None,
                    attachments=None,
                    headers=None,
                    cc=None,
                    reply_to=None
                )
                email_sent = email.send()
                emails_sent += email_sent

                if bool(email_sent):
                    Communication.objects.create(
                        order=self.order,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to_email=[email_address],
                        subject=subject,
                        body=body
                    )

        return (
            bool(len(email_addresses)) and (emails_sent == len(email_addresses))
        )
