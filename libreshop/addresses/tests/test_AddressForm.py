from unittest.mock import patch
from django.forms import Textarea
from django.test import TestCase
from django_countries import Countries
from django_countries.widgets import CountrySelectWidget
from ..forms import AddressForm
from ..models import Address

# Create your tests here.
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


    def test_locality_field_is_displayed(self):
        '''
        Test that the `locality` field is displayed on the form.
        '''
        form = AddressForm()

        fields = form._meta.fields

        self.assertIn('locality', fields)


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


    def test_locality_field_has_custom_label(self):
        '''
        Test that the `locality` field has a custom label.
        '''
        form = AddressForm()

        labels = form._meta.labels
        label = labels.get('locality', None)

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
    def test_form_does_not_require_postal_code_for_ireland(self, clean_mock):
        '''
        Test that a postal code is optional for the country of Ireland.
        '''
        form = AddressForm()
        cleaned_data = {
            'country': 'IE',
            'postal_code': None,
        }
        clean_mock.return_value = cleaned_data

        form.clean()

        form_errors = form.errors.get('postal_code')
        self.assertIsNone(form_errors)


    @patch('django.forms.ModelForm.clean')
    def test_form_nullifies_postal_code_for_ireland(self, clean_mock):
        '''
        Test that a postal code is nullified when data is entered for this
        field and the country of Ireland is selected, since a postal code is not
        used in Ireland.
        '''
        form = AddressForm()
        cleaned_data = {
            'country': 'IE',
            'postal_code': '12345',
        }
        clean_mock.return_value = cleaned_data

        cleaned_data = form.clean()

        postal_code = cleaned_data.get('postal_code')
        self.assertIsNone(postal_code)


class AddressFormPostalCodeFieldTest(TestCase):

    def get_form_errors(self, country, postal_code):
        '''
        Utility function to calculate the AddressForm.errors dict.
        '''
        form = AddressForm()
        cleaned_data = {
            'country': country,
            'postal_code': postal_code,
        }

        with patch('django.forms.ModelForm.clean') as clean_mock:
            clean_mock.return_value = cleaned_data
            cleaned_data = form.clean()

        form_errors = form.errors.get('postal_code')

        return form_errors


    def assert_valid(self, country, postal_code):
        form_errors = self.get_form_errors(country, postal_code)
        self.assertIsNone(form_errors)


    def assert_invalid(self, country, postal_code):
        form_errors = self.get_form_errors(country, postal_code)
        self.assertIsNotNone(form_errors)


    def test_form_properly_validates_postal_codes_used_for_the_united_states(self):
        '''
        Test that an error is added to the AddressForm when an invalid Postal
        Code is used for The United States.
        '''
        self.assert_valid('US', '12345')
        self.assert_valid('US', '12345-1234')

        self.assert_invalid('US', '1234')
        self.assert_invalid('US', '123456')
        self.assert_invalid('US', '1234a')
        self.assert_invalid('US', '12345-')
        self.assert_invalid('US', '12345-1')
        self.assert_invalid('US', '12345-12')
        self.assert_invalid('US', '12345-123')
        self.assert_invalid('US', '12345 1')
        self.assert_invalid('US', '12345 12')
        self.assert_invalid('US', '12345 123')
