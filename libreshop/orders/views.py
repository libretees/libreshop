import importlib
import logging
import random
import braintree
from collections import Counter
from decimal import Decimal, ROUND_CEILING
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.views.generic import FormView, TemplateView
import easypost
from ipware.ip import get_real_ip
from measurement.measures import Weight
from addresses.forms import AddressForm
from addresses.models import Address
from carts.utils import SessionCart
from products.models import Variant
from .forms import OrderReceiptForm, PaymentForm
from .models import Order, Purchase, TaxRate, Transaction

# Set a universally unique identifier (UUID).
UUID = '9bf75036-ec58-4188-be12-4f983cac7e55'

easypost.api_key = settings.EASYPOST_API_KEY

# Initialize logger.
logger = logging.getLogger(__name__)

def create_address(address_info, verify=['delivery']):

    address = None
    try:
        street_address = address_info['street_address'].split('\r\n', 1)
        address = easypost.Address.create(
            verify=verify,
            name = address_info['recipient_name'],
            street1 = street_address[0],
            street2 = (
                street_address[1] if len(street_address) > 1 else None
            ),
            city = address_info['locality'],
            state = address_info['region'],
            zip = address_info['postal_code'],
            country = address_info['country']
        )
    except easypost.Error as e:
        error = e.json_body.get('error')
        if error is not None:
            error_code = error.get('code')
            if error_code == 'ADDRESS.VERIFY.INTL_NOT_ENABLED':
                logger.info('Retrying address creation without delivery validation...')
                address = create_address(address_info, verify=None)
            else:
                logger.error('Error received from Easypost API (%s).' % str(e))

    return address


def create_customs_items(products):

    products_aggregate = Counter(product.name for product in products)

    customs_items = list()
    for item_name, quantity in products_aggregate.items():
        product = next(
            product for product in products if product.name == item_name
        )
        product_weight = Weight(g=product.weight * quantity)

        customs_item = easypost.CustomsItem.create(
            description=product.name,
            quantity=quantity,
            value=product.price * quantity,
            weight=max(0.1, product_weight.oz),
            origin_country='US'
        )
        customs_items.append(customs_item)

    return customs_items


def get_shipping_rate(address, products):

    shipping_weight = Weight(g=sum([
        product.weight for product in products])
    )

    to_address = create_address(address)
    from_address = create_address({
        'recipient_name': 'LibreTees',
        'street_address': '2111 Jefferson Davis Hwy\r\nApt 405S',
        'locality': 'Arlington',
        'region': 'VA',
        'postal_code': '22202',
        'country': 'US',
        'phone': '888-995-4273'
    })

    customs_info = None
    if to_address.country != from_address.country:
        customs_items = create_customs_items(products)
        customs_info = easypost.CustomsInfo.create(
            customs_certify=True,
            customs_signer='libreshop',
            contents_type='merchandise',
            restriction_type='none',
            restriction_comments='',
            customs_items=customs_items
        )

    parcel = easypost.Parcel.create(
        predefined_package='Parcel',
        weight=shipping_weight.oz
    )

    shipment = easypost.Shipment.create(
        to_address = to_address,
        from_address = from_address,
        parcel = parcel,
        customs_info = customs_info
    )

    rate_info = shipment.lowest_rate()

    return float(rate_info.rate)


def calculate_shipping_cost(*args, **kwargs):

    products = kwargs.pop('products', [])

    results = []
    for api_name, supplier in settings.FULFILLMENT_BACKENDS:
        kwargs.update({
            'products': [
                product for product in products if supplier in product.suppliers
            ]
        })
        try:
            module = importlib.import_module(api_name)
            logger.debug('Calling \'%s.get_shipping_rate\'...' % api_name)
            result = module.get_shipping_rate(*args, **kwargs)
            logger.debug('Called \'%sget_shipping_rate\'.' % api_name)
        except ImportError as e:
            logger.critical('Unable to import module \'%s\'.' % api_name)
        except KeyError as e:
            logger.critical(
                'KeyError within \'%s.%s\' backend: %s' %
                (module_name, attribute_name, e))
        else:
            results.append(result)

    manufactured_products = [
        product for product in products if not product.suppliers
    ]

    if manufactured_products:
        address = kwargs.pop('address')
        rate = get_shipping_rate(address, manufactured_products)
        results.append(rate)

    return (
        Decimal(sum(results)).quantize(Decimal('1.00'), rounding=ROUND_CEILING)
        if len(results) else Decimal(0.00)
    )


# Create views here.
class ConfirmationView(FormView):

    form_class = OrderReceiptForm
    template_name = 'orders/confirmation.html'


    def get_form_kwargs(self):
        kwargs = super(ConfirmationView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'request': self.request
            })
        return kwargs


    def get_success_url(self):
        next_url = self.request.POST.get(
            'next', reverse('checkout:confirmation')
        )
        return next_url


    def get_context_data(self, **kwargs):
        context = super(ConfirmationView, self).get_context_data(**kwargs)

        session_data = self.request.session.get(UUID)
        if session_data:
            email_address = session_data.get('email_address')
            order_token = session_data.get('order_token')
            if order_token:
                order = Order.objects.get(token=order_token)
                purchases = Purchase.objects.filter(order=order)
                context.update({
                    'email_address': email_address,
                    'order': order,
                    'purchases': purchases,
                })

        return context


class CheckoutFormView(FormView):

    form_class = AddressForm
    template_name = 'orders/checkout.html'
    success_url = '/'

    def __init__(self, *args, **kwargs):
        super(CheckoutFormView, self).__init__(*args, **kwargs)

        self.client_token = braintree.ClientToken.generate()
        self.deleted_data = None


    def get(self, request, *args, **kwargs):

        deleted_steps = [
            key for key in request.GET if key in self.request.session[UUID]
        ]
        for key in deleted_steps:
            self.delete_previous_step(key)

        template_response = None
        if deleted_steps:
            template_response = self.load_previous_step()

        return (
            super(CheckoutFormView, self).get(request, *args, **kwargs)
            if not template_response else template_response
        )


    def post(self, request, *args, **kwargs):

        template_response = None

        if not self.session_data_is_valid():
            template_response = self.load_previous_step()

        return (
            super(CheckoutFormView, self).post(request, *args, **kwargs)
            if not template_response else template_response
        )


    def dispatch(self, request, *args, **kwargs):

        if not self.request.session.has_key(UUID):
            self.request.session[UUID] = {}

        self.cart = SessionCart(self.request.session)
        self.subtotal = self.cart.total

        self.shipping_address = self.request.session[UUID].get('shipping')

        self.shipping_cost = Decimal(0.00)
        self.sales_tax = Decimal(0.00)
        self.total = Decimal(0.00)

        if self.shipping_address:

            # Calculate the shipping cost.
            self.shipping_cost = calculate_shipping_cost(
                address=self.shipping_address,
                products=self.cart
            )

            # Reset 'shipping' step, if no shipping cost could be calculated.
            if not self.shipping_cost:
                self.shipping_address = None
                del self.request.session[UUID]['shipping']
                self.request.session.modified = True

            # Otherwise, calculate sales tax, if the user is based in the US.
            elif self.shipping_address['country'] == 'US':
                # Disregard any ZIP+4 information.
                zip_code = self.shipping_address['postal_code'].split('-')[0]

                tax_rates = {
                    tax_rate.postal_code:tax_rate.tax_rate
                    for tax_rate in TaxRate.objects.all()
                }
                if zip_code in tax_rates:
                    sales_tax_rate = Decimal(0.06)
                    sales_tax = self.subtotal * sales_tax_rate
                    self.sales_tax = Decimal(sales_tax).quantize(
                        Decimal('1.00'), rounding=ROUND_CEILING
                    )

        self.total = (
            self.subtotal + self.shipping_cost + self.sales_tax
        )

        self.steps = (
            {
                'name': 'shipping',
                'form_class': AddressForm,
                'template': 'orders/checkout.html',
                'context': {
                    'description': 'where are we sending this?',
                }
            },
            {
                'name': 'payment',
                'form_class': PaymentForm,
                'template': 'orders/checkout.html',
                'form_kwargs': {
                    'amount': self.total
                },
                'context': {
                    'description': 'how are you paying?',
                    'client_token': self.client_token,
                    'shipping_cost': self.shipping_cost,
                    'sales_tax': self.sales_tax,
                    'total': self.total
                }
            },
        )

        self.current_step = self.get_current_step()

        return super(CheckoutFormView, self).dispatch(request, *args, **kwargs)


    def get_current_step(self):
        '''
        Get the current step within the form wizard.
        '''
        completed_steps = self.request.session.get(UUID, {})

        remaining_steps = [
            step for step in self.steps if step['name'] not in completed_steps
        ]
        current_step = remaining_steps[0] if remaining_steps else None

        logger.debug('Completed steps: %s' % ', '.join(step for step in completed_steps))
        logger.debug('Remaining steps: %s' % ', '.join(step['name'] for step in remaining_steps))
        logger.debug('Current step: %s' % (current_step['name'] if current_step else ''))

        return current_step


    def get_template_names(self):
        template_name = self.current_step['template']

        return [template_name]


    def get_form_class(self):
        logger.debug('Getting form class...')
        return self.current_step['form_class']


    def get_form_kwargs(self):
        kwargs = super(CheckoutFormView, self).get_form_kwargs()

        if 'form_kwargs' in self.current_step:
            kwargs.update(self.current_step['form_kwargs'])

        return kwargs


    def get_form(self, form_class=None):
        '''
        Get the Form object that will be supplied to the FormView's context.
        '''
        # Instantiate Form.
        form = super(CheckoutFormView, self).get_form(form_class=form_class)

        if isinstance(form, AddressForm):
            # Determine the IP address associated to the HTTP Request.
            ip_address = get_real_ip(self.request)
    
            # Populate the form's `country` field with the user's apparent
            # location.
            if ip_address and not form.is_bound:
                geo_ip2 = GeoIP2()
                location = geo_ip2.country(ip_address)
                form.fields['country'].initial = location['country_code']

        logger.debug(
            'Got %s %s form' % (
                'bound' if form.is_bound else 'unbound', form.__class__.__name__
            )
        )

        return form


    def form_valid(self, form):

        self.request.session[UUID].update({
            self.current_step['name']: form.cleaned_data,
        })
        self.request.session.modified = True

        # Create an order if there are no more steps to complete.
        if not self.get_current_step():
            shipping_address = Address.objects.create(**self.shipping_address)
            order = Order.objects.create(
                shipping_address=shipping_address,
                subtotal=self.subtotal,
                sales_tax=self.sales_tax,
                shipping_cost=self.shipping_cost,
                total=self.total
            )

            self.order_token = order.token

            for variant in self.cart:
                purchase = Purchase.objects.create(
                    order=order,
                    variant=variant,
                    price=variant.price
                )

            Transaction.objects.create(
                order=order,
                transaction_id=form.cleaned_data.get('transaction_id'),
                amount=form.cleaned_data.get('amount'),
                cardholder_name=form.cleaned_data.get('cardholder_name'),
                country=form.cleaned_data.get('country'),
                payment_card_type=form.cleaned_data.get('payment_card_type'),
                payment_card_last_4=form.cleaned_data.get('payment_card_last_4'),
                payment_card_expiration_date=form.cleaned_data.get(
                    'payment_card_expiration_date'
                ),
                created_at = form.cleaned_data.get('created_at'),
                origin_ip_address = get_real_ip(self.request),
                authorized = form.cleaned_data.get('authorized')
            )

        return super(CheckoutFormView, self).form_valid(form)


    def session_data_is_valid(self):

        session_data = self.request.session.get(UUID, None)

        is_valid = True
        if session_data:
            completed_steps = [
                step for step in self.steps if step['name'] in session_data
            ]

            for completed_step in completed_steps:
                step_name = completed_step['name']
                form_class = completed_step['form_class']

                form = form_class(data=session_data[step_name])
                if not form.is_valid():
                    is_valid = False
                    break

        return is_valid


    def delete_previous_step(self, key=None):
        '''
        '''
        session_data = self.request.session[UUID]

        if not key:
            previous_index = self.steps.index(self.current_step)-1
            key = self.steps[previous_index]['name']

        if key in session_data:
            self.deleted_data = session_data.get(key, None)
            del session_data[key]
            self.request.session.modified = True

        self.current_step = self.get_current_step()


    def load_previous_step(self):
        '''
        '''
        self.delete_previous_step()

        form_class = self.get_form_class()
        form = form_class(data=self.deleted_data)

        if not form.is_valid():
            form.add_error(None, 'Something went wrong here...')

        template_names = self.get_template_names()
        context_data = self.get_context_data(form=form)

        template_response = TemplateResponse(
            self.request, template_names, context_data
        )

        return template_response


    def get_success_url(self):
        logger.info('Getting Success URL...')

        if self.get_current_step():
            url = reverse('checkout:main')
        else:
            # Empty the cart.
            self.cart.empty()

            # Delete all CheckoutFormView Session Data.
            del self.request.session[UUID]

            # Add the Order Token to CheckoutFormView Session Data.
            self.request.session[UUID] = {
                'order_token': self.order_token
            }

            url = reverse('checkout:confirmation')

        logger.info('Redirecting to %s' % url)

        return url


    def get_context_data(self, **kwargs):
        context = super(CheckoutFormView, self).get_context_data(**kwargs)

        current_position = next(
            i for (i, step) in enumerate(self.steps)
            if step['name'] == self.current_step['name']
        )

        context.update({
            'cart': self.cart,
            'subtotal': self.subtotal,
            'current_position': current_position,
            'steps': enumerate(self.steps),
        })

        step_context = self.current_step['context']
        if step_context:
            context.update(step_context)

        return context
