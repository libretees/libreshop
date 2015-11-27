from operator import itemgetter
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.utils import importlib
from django.views.generic import FormView
from ipware.ip import get_real_ip
from .forms import AddressForm

# Create your views here.
class AddressFormView(FormView):

    template_name = 'addresses/address_form.html'
    success_url = '/'

    def get_form(self):
        form = AddressForm(**self.get_form_kwargs())

        ip_address = get_real_ip(self.request)
        if ip_address and not form.is_bound:
            geo_ip2 = GeoIP2()
            location = g.country(ip_address)
            form.fields['country'].initial = location['country_code']

        return form


class ShippingAddressFormView(AddressFormView):

    def form_valid(self, form):
        self.request.session['shipping_address'] = form.cleaned_data
        return super(ShippingAddressFormView, self).form_valid(form)


    def calculate_shipping_cost(weight, width, depth, height):

        results = []
        for api in settings.SHIPPING_APIS:
           module_name, attribute_name = itemgetter(0, 1)(api.split('.'))
           module = importlib.import_module(module_name)
           function = getattr(module, attribute_name)
           result = function(weight, width, depth, height)
           results.append(result)

        return results


class BillingAddressFormView(AddressFormView):

    def form_valid(self, form):
        self.request.session['billing_address'] = form.cleaned_data
        return super(BillingAddressFormView, self).form_valid(form)
