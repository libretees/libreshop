from django.contrib.gis.geoip2 import GeoIP2
from django.shortcuts import render
from django.views.generic import FormView
from ipware.ip import get_real_ip
from .forms import AddressForm

# Create your views here.
class ShippingAddressView(FormView):

    template_name = 'addresses/shipping_address.html'

    def get_form(self):
        form = AddressForm(**self.get_form_kwargs())

        ip_address = get_real_ip(self.request)
        if ip_address and not form.is_bound:
            g = GeoIP2()
            location = g.city(ip_address)
            form.fields['locality'].initial = location['city']
            form.fields['postal_code'].initial = location['postal_code']
            form.fields['region'].initial = location['region']
            form.fields['country'].initial = location['country_code']

        return form
