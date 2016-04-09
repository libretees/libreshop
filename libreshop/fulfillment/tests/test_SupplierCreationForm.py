from django.conf import settings
from django.test import TestCase
from .. import forms

try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch

class SupplierCreationFormTest(TestCase):

    @patch.object(forms, 'settings')
    def test_form_loads_valid_fulfillment_backend_choices_from_settings(self, settings_mock):
        '''
        Test that SupplierCreationForm creates a select <option> markup for
        valid backend choices.
        '''
        form = forms.SupplierCreationForm()

        backend = ('django.core.mail.backends.locmem.EmailBackend', 'Email')
        settings_mock.FULFILLMENT_BACKENDS = [backend]

        expected_markup = '<option value="%s">%s</option>' % backend
        form_markup = str(form)

        self.assertIn(expected_markup, form_markup)


    @patch.object(forms, 'settings')
    def test_form_filters_backend_choices_for_invalid_modules(self, settings_mock):
        '''
        Test that SupplierCreationForm filters out invalid backend choices, if
        a module has been specified that is not importable.
        '''
        settings_mock.FULFILLMENT_BACKENDS = [('foo', 'foo')]
        form = forms.SupplierCreationForm()
        form_markup = str(form)
        self.assertNotIn('foo', form_markup)


    @patch.object(forms, 'settings')
    def test_form_filters_backend_choices_for_invalid_attributes(self, settings_mock):
        '''
        Test that SupplierCreationForm filters out invalid backend choices, if
        an attribute has been specified that is not importable.
        '''
        settings_mock.FULFILLMENT_BACKENDS = [
            ('django.core.mail.backends.locmem.foo', 'foo')
        ]
        form = forms.SupplierCreationForm()
        form_markup = str(form)
        self.assertNotIn('foo', form_markup)
