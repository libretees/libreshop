import importlib
import logging
from operator import itemgetter
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.views.generic import FormView
from ipware.ip import get_real_ip
from .forms import AddressForm

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your views here.
class AddressFormView(FormView):

    template_name = 'addresses/address_form.html'
    success_url = '/'

    def get_form(self):
        '''
        Get the Form object that will be supplied to the FormView's context.
        '''
        # Instantiate Form.
        form = AddressForm(**self.get_form_kwargs())

        # Determine the IP address associated to the HTTP Request.
        ip_address = get_real_ip(self.request)

        # Populate the form's `country` field with the user's apparent location.
        if ip_address and not form.is_bound:
            geo_ip2 = GeoIP2()
            location = geo_ip2.country(ip_address)
            form.fields['country'].initial = location['country_code']

        return form


class ShippingAddressFormView(AddressFormView):

    def form_valid(self, form):
        self.request.session['shipping_address'] = form.cleaned_data
        return super(ShippingAddressFormView, self).form_valid(form)


class BillingAddressFormView(AddressFormView):

    def form_valid(self, form):
        self.request.session['billing_address'] = form.cleaned_data
        return super(BillingAddressFormView, self).form_valid(form)


def calculate_shipping_cost(*args, **kwargs):

    results = []
    for api_name in settings.SHIPPING_APIS:
        index = api_name.rfind('.')
        module_name, attribute_name = api_name[:index], api_name[index+1:]
        module, function = None, None
        try:
            module = importlib.import_module(module_name)
            function = getattr(module, attribute_name)
        except ImportError as e:
            logger.critical('Unable to import module \'%s\'.' % module_name)
        except AttributeError as e:
            logger.critical('\'%s\' module has no attribute \'%s\'.' %
                (module_name, attribute_name))
        else:
            logger.info('Calling \'%s.%s\'...' % (module_name, attribute_name))
            result = function(*args, **kwargs)
            logger.info('Called \'%s.%s\'.' % (module_name, attribute_name))
            results.append(result)

    return results
