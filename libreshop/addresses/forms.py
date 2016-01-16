import logging
import re
from django import forms
from . import models
from django_countries import Countries
from django_countries.widgets import CountrySelectWidget

# Initialize logger
logger = logging.getLogger(__name__)

# Define regex patterns for postal codes, specific to each country.
POSTAL_CODE_PATTERNS = {
    'US': r'^[0-9]{5}(?:-[0-9]{4})?$',
}


class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = ('recipient_name', 'street_address', 'locality', 'region',
            'postal_code', 'country',
        )
        labels = {
            'recipient_name': 'Recipient',
            'street_address': 'Address',
            'locality':       'City/Town',
            'region':         'State/Province/County',
            'postal_code':    'ZIP/Postcode/Postal Code',
        }
        widgets = {
            'street_address': forms.Textarea(attrs={'rows': 4,}),
            'country':        CountrySelectWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.required:
                field.error_messages.update({
                    'required': 'The %s field is required.' % field.label,
                })


    def validate_postal_code(self, country, postal_code):

        pattern = POSTAL_CODE_PATTERNS.get(country)
        if pattern:
            regex = re.compile(pattern, re.VERBOSE)
            match = re.match(regex, postal_code)
            if not match:
                error_message = (
                    ('The %s specified (%s) is invalid for the selected '
                     'country (%s).') %
                    (self.postal_code_label, postal_code, self.country_name)
                )
                self.add_error('postal_code', error_message)


    def clean(self):
        self.cleaned_data = super(AddressForm, self).clean()

        country = self.cleaned_data.get('country')
        postal_code = self.cleaned_data.get('postal_code')

        self.postal_code_label = self.fields['postal_code'].label
        self.country_name = Countries().name(country)
        if country and country != 'IE' and not postal_code:
            error_message = (
                ('The %s field is required for addresses within the selected '
                 'country (%s).') % (self.postal_code_label, self.country_name)
            )
            self.add_error('postal_code', error_message)
        elif country == 'IE' and postal_code:
            self.cleaned_data.update({
                'postal_code': None,
            })
        else:
            self.validate_postal_code(country, postal_code)

        return self.cleaned_data
