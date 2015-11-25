from importlib import import_module
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
from ..forms import AddressForm
from ..views import AddressFormView, ShippingAddressFormView


# Create your tests here.
class ShippingAddressFormViewTest(TestCase):

    def test_view_extends_addressformview(self):
        '''
        Test that the View extends addresses.views.AddressFormView.
        '''
        view = ShippingAddressFormView()

        self.assertIsInstance(view, AddressFormView)


    def test_valid_form_cleaned_data_is_saved_within_request_session(self):
        '''
        Test that all form.cleaned_data values are saved within the
        request.session variable.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        view = ShippingAddressFormView()
        view.request = request
        form_data = {
            'foo': 'bar',
        }
        form = AddressForm(data=form_data)
        form.cleaned_data = form_data

        view.form_valid(form)

        shipping_address = request.session.get('shipping_address')

        self.assertEqual(shipping_address, {'foo': 'bar'})
