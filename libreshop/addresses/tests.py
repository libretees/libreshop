from unittest.mock import patch
from django.forms import Textarea
from django.http import HttpRequest
from django.test import TestCase
from django_countries import Countries
from django_countries.widgets import CountrySelectWidget
from .models import Address
from .forms import AddressForm
from .views import ShippingAddressView

# Create your tests here.
class AddressModelTest(TestCase):

    def test_model_plural_name_is_addresses(self):
        '''
        Test that Address model has 'addresses' set as its plural name.
        '''
        address = Address()
        plural_name = address._meta.verbose_name_plural
        self.assertEqual(plural_name, 'addresses')


    def test_model_has_customer_field(self):
        '''
        Test that Address.customer is present.
        '''
        address = Address()
        customer = None
        try:
            customer = address._meta.get_field('customer')
        except:
            pass
        self.assertIsNotNone(customer)


    def test_model_customer_field_is_not_required(self):
        '''
        Test that Address.customer is not required.
        '''
        address = Address()
        customer = None
        try:
            customer = address._meta.get_field('customer')
        except:
            pass
        nullable = getattr(customer, 'null', None)
        self.assertTrue(nullable)


    def test_model_customer_field_can_be_blank(self):
        '''
        Test that Address.customer allows blank values in forms.
        '''
        address = Address()
        customer = None
        try:
            customer = address._meta.get_field('customer')
        except:
            pass
        blank = getattr(customer, 'blank', None)
        self.assertTrue(blank)


    def test_model_has_recipient_name_field(self):
        '''
        Test that Address.recipient_name is present.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        self.assertIsNotNone(recipient_name)


    def test_model_recipient_name_field_is_not_required(self):
        '''
        Test that Address.recipient_name is not required.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        nullable = getattr(recipient_name, 'null', None)
        self.assertTrue(nullable)


    def test_model_recipient_name_field_can_be_blank(self):
        '''
        Test that Address.recipient_name allows blank values in forms.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        blank = getattr(recipient_name, 'blank', None)
        self.assertTrue(blank)


    def test_model_recipient_name_field_has_max_length(self):
        '''
        Test that Address.recipient_name max length is 64.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        max_length = getattr(recipient_name, 'max_length', None)
        self.assertEqual(max_length, 64)


    def test_model_has_street_address_field(self):
        '''
        Test that Address.street_address is present.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        self.assertIsNotNone(street_address)


    def test_model_street_address_field_is_required(self):
        '''
        Test that Address.street_address is required.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        nullable = getattr(street_address, 'null', None)
        self.assertFalse(nullable)


    def test_model_street_address_field_cannot_be_blank(self):
        '''
        Test that Address.street_address does not allow blank values in forms.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        blank = getattr(street_address, 'null', None)
        self.assertFalse(blank)


    def test_model_street_address_field_has_max_length(self):
        '''
        Test that Address.street_address max length is 1024.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        max_length = getattr(street_address, 'max_length', None)
        self.assertEqual(max_length, 1024)


    def test_model_has_municipality_field(self):
        '''
        Test that Address.municipality is present.
        '''
        address = Address()
        municipality = None
        try:
            municipality = address._meta.get_field('municipality')
        except:
            pass
        self.assertIsNotNone(municipality)


    def test_model_municipality_field_is_required(self):
        '''
        Test that Address.municipality is required.
        '''
        address = Address()
        municipality = None
        try:
            municipality = address._meta.get_field('municipality')
        except:
            pass
        nullable = getattr(municipality, 'null', None)
        self.assertFalse(nullable)


    def test_model_municipality_field_cannot_be_blank(self):
        '''
        Test that Address.municipality does not allow blank values in forms.
        '''
        address = Address()
        municipality = None
        try:
            municipality = address._meta.get_field('municipality')
        except:
            pass
        blank = getattr(municipality, 'null', None)
        self.assertFalse(blank)


    def test_model_municipality_field_has_max_length(self):
        '''
        Test that Address.municipality max length is 16.
        '''
        address = Address()
        municipality = None
        try:
            municipality = address._meta.get_field('municipality')
        except:
            pass
        max_length = getattr(municipality, 'max_length', None)
        self.assertEqual(max_length, 16)


    def test_model_has_region_field(self):
        '''
        Test that Address.region is present.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        self.assertIsNotNone(region)


    def test_model_region_field_is_required(self):
        '''
        Test that Address.region is required.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        nullable = getattr(region, 'null', None)
        self.assertFalse(nullable)


    def test_model_region_field_cannot_be_blank(self):
        '''
        Test that Address.region does not allow blank values in forms.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        blank = getattr(region, 'null', None)
        self.assertFalse(blank)


    def test_model_region_field_has_max_length(self):
        '''
        Test that Address.region max length is 16.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        max_length = getattr(region, 'max_length', None)
        self.assertEqual(max_length, 16)


    def test_model_has_postal_code_field(self):
        '''
        Test that Address.postal_code is present.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        self.assertIsNotNone(postal_code)


    def test_model_postal_code_field_is_not_required(self):
        '''
        Test that Address.postal_code is not required.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        nullable = getattr(postal_code, 'null', None)
        self.assertTrue(nullable)


    def test_model_postal_code_field_can_be_blank(self):
        '''
        Test that Address.postal_code allows blank values in forms.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        blank = getattr(postal_code, 'blank', None)
        self.assertTrue(blank)


    def test_model_postal_code_field_has_max_length(self):
        '''
        Test that Address.postal_code max length is 16.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        max_length = getattr(postal_code, 'max_length', None)
        self.assertEqual(max_length, 16)


    def test_model_has_country_field(self):
        '''
        Test that Address.country is present.
        '''
        address = Address()
        country = None
        try:
            country = address._meta.get_field('country')
        except:
            pass
        self.assertIsNotNone(country)


    def test_model_country_field_is_required(self):
        '''
        Test that Address.country is required.
        '''
        address = Address()
        country = None
        try:
            country = address._meta.get_field('country')
        except:
            pass
        nullable = getattr(country, 'null', None)
        self.assertFalse(nullable)


    def test_model_country_field_cannot_be_blank(self):
        '''
        Test that Address.country does not allow blank values in forms.
        '''
        address = Address()
        country = None
        try:
            country = address._meta.get_field('country')
        except:
            pass
        blank = getattr(country, 'null', None)
        self.assertFalse(blank)


class ShippingAddressViewTest(TestCase):

    def test_view_uses_addressform_form(self):
        '''
        Test that the view uses addresses.forms.AddressForm.
        '''
        request = HttpRequest()
        view = ShippingAddressView()
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
        view = ShippingAddressView()
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
        view = ShippingAddressView()
        view.request = request
        get_real_ip_mock.return_value = None

        form = view.get_form()

        selected_option = ('<option value="" selected="selected">'
            '---------</option>')
        self.assertIn(selected_option, str(form))


    @patch('addresses.views.get_real_ip')
    @patch.object(ShippingAddressView, 'get_form_kwargs')
    def test_bound_form_does_not_geolocate_users_country(
        self, get_form_kwargs_mock, get_real_ip_mock):
        '''
        Test that the view does not perform geolocation when it is processing a
        bound form.
        '''
        request = HttpRequest()
        view = ShippingAddressView()
        view.request = request
        get_real_ip_mock.return_value = '127.0.0.1'
        get_form_kwargs_mock.return_value = {'data': request.POST}

        form = view.get_form()

        selected_option = ('<option value="" selected="selected">'
            '---------</option>')
        self.assertIn(selected_option, str(form))


class AddressFormTest(TestCase):

    def test_form_uses_Address_model(self):
        '''
        Test that addresses.forms.AddressForm is a ModelForm for the
        addresses.Address model.
        '''
        form = AddressForm()

        model = form._meta.model

        self.assertEqual(model, Address)


    def test_recipient_name_field_is_displayed(self):
        '''
        Test that the `recipient_name` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('recipient_name', fields)


    def test_street_address_field_is_displayed(self):
        '''
        Test that the `street_address` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('street_address', fields)


    def test_municipality_field_is_displayed(self):
        '''
        Test that the `municipality` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('municipality', fields)


    def test_region_field_is_displayed(self):
        '''
        Test that the `region` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('region', fields)


    def test_postal_code_field_is_displayed(self):
        '''
        Test that the `postal_code` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('postal_code', fields)


    def test_country_field_is_displayed(self):
        '''
        Test that the `country` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('country', fields)


    def test_recipient_name_field_has_custom_label(self):
        '''
        Test that the `recipient_name` field has a custom label.
        '''
        form = AddressForm()

        labels = form._meta.labels
        label = labels.get('recipient_name', None)

        self.assertIsNotNone(label)


    def test_street_address_field_has_custom_label(self):
        '''
        Test that the `street_address` field has a custom label.
        '''
        form = AddressForm()

        labels = form._meta.labels
        label = labels.get('street_address', None)

        self.assertIsNotNone(label)


    def test_municipality_field_has_custom_label(self):
        '''
        Test that the `municipality` field has a custom label.
        '''
        form = AddressForm()

        labels = form._meta.labels
        label = labels.get('municipality', None)

        self.assertIsNotNone(label)


    def test_region_field_has_custom_label(self):
        '''
        Test that the `region` field has a custom label.
        '''
        form = AddressForm()

        labels = form._meta.labels
        label = labels.get('region', None)

        self.assertIsNotNone(label)


    def test_postal_code_field_has_custom_label(self):
        '''
        Test that the `postal_code` field has a custom label.
        '''
        form = AddressForm()

        labels = form._meta.labels
        label = labels.get('postal_code', None)

        self.assertIsNotNone(label)


    def test_street_address_field_uses_textarea_widget(self):
        '''
        Test that the `street_address` field uses a Textarea widget.
        '''
        form = AddressForm()

        widgets = form._meta.widgets
        widget = widgets.get('street_address', None)

        self.assertIsInstance(widget, Textarea)


    def test_country_field_uses_countryselectwidget_widget(self):
        '''
        Test that the `country` field uses a CountrySelectWidget widget.
        '''
        form = AddressForm()

        widgets = form._meta.widgets
        widget = widgets.get('country', None)

        self.assertIsInstance(widget, CountrySelectWidget)


    def test_required_fields_have_custom_error_message(self):
        '''
        Test that required form fields display a custom error message specific
        to that field.
        '''
        form = AddressForm()
        error_messages = [
            str(field.error_messages['required']) for field
            in form.fields.values() if field.required
        ]

        custom_error_messages = [
            'The %s field is required.' % field.label for field
            in form.fields.values() if field.required
        ]

        self.assertEqual(error_messages, custom_error_messages)


    def test_optional_fields_have_standard_error_message(self):
        '''
        Test that optional form fields do not have a custom error message set.
        '''
        form = AddressForm()
        error_messages = [
            str(field.error_messages['required']) for field
            in form.fields.values() if not field.required
        ]

        standard_error_messages = ['This field is required.']
        standard_error_messages *= len(error_messages)

        self.assertEqual(error_messages, standard_error_messages)


    @patch('django.forms.ModelForm.clean')
    def test_form_requires_postal_code_for_all_countries_except_ireleand(self,
        clean_mock):
        '''
        Test that all countries other than Ireland must specify a postal code.
        '''
        form = AddressForm()
        cleaned_data = {
            'country': 'US',
            'postal_code': None,
        }
        form.cleaned_data = cleaned_data
        clean_mock.return_value = cleaned_data

        form.clean()

        label = form.fields['postal_code'].label
        country_name = Countries().name(cleaned_data['country'])
        error_message = (
            ('The %s field is required for addresses within the selected '
             'country (%s).') % (label, country_name)
        )
        form_errors = form.errors.get('postal_code')

        self.assertIn(error_message, form_errors)


    @patch('django.forms.ModelForm.clean')
    def test_form_does_not_require_postal_code_for_ireleand(self, clean_mock):
        '''
        Test that a postal code is optional for the country of Ireland.
        '''
        form = AddressForm()
        cleaned_data = {
            'country': 'IE',
            'postal_code': None,
        }
        form.cleaned_data = cleaned_data
        clean_mock.return_value = cleaned_data

        form.clean()

        form_errors = form.errors.get('postal_code')

        self.assertIsNone(form_errors)
