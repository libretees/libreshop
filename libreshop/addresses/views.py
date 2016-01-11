import logging
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
