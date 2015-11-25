from unittest.mock import patch
from django.http import HttpRequest
from django.test import TestCase
from ..forms import AddressForm
from ..views import AddressFormView


# Create your tests here.
class AddressFormViewTest(TestCase):

    def test_view_uses_addressform_form(self):
        '''
        Test that the view uses addresses.forms.AddressForm.
        '''
        request = HttpRequest()
        view = AddressFormView()
        view.request = request

        form = view.get_form()

        self.assertIsInstance(form, AddressForm)


    @patch('addresses.views.get_real_ip')
    @patch('addresses.views.GeoIP2.country')
    def test_unbound_form_defaults_to_users_country_if_ip_found(
        self, country_mock, get_real_ip_mock):
        '''
        Test that the view geolocates the user's country when a valid IP is
        returned by the `django-ipware` package.
        '''
        request = HttpRequest()
        view = AddressFormView()
        view.request = request
        get_real_ip_mock.return_value = '127.0.0.1'
        country_mock.return_value = {
            'country_name': 'United States', 'country_code': 'US'
        }

        form = view.get_form()

        selected_option = ('<option value="US" selected="selected">'
                    'United States of America</option>')
        self.assertIn(selected_option, str(form))


    @patch('addresses.views.get_real_ip')
    def test_unbound_form_does_not_geolocate_if_ip_not_found(
        self, get_real_ip_mock):
        '''
        Test that the view does not perform geolocation when a valid IP cannot
        be determined.
        '''
        request = HttpRequest()
        view = AddressFormView()
        view.request = request
        get_real_ip_mock.return_value = None

        form = view.get_form()

        selected_option = ('<option value="" selected="selected">'
            '---------</option>')
        self.assertIn(selected_option, str(form))


    @patch('addresses.views.get_real_ip')
    @patch.object(AddressFormView, 'get_form_kwargs')
    def test_bound_form_does_not_geolocate_users_country(
        self, get_form_kwargs_mock, get_real_ip_mock):
        '''
        Test that the view does not perform geolocation when it is processing a
        bound form.
        '''
        request = HttpRequest()
        view = AddressFormView()
        view.request = request
        get_real_ip_mock.return_value = '127.0.0.1'
        get_form_kwargs_mock.return_value = {'data': request.POST}

        form = view.get_form()

        selected_option = ('<option value="" selected="selected">'
            '---------</option>')
        self.assertIn(selected_option, str(form))
