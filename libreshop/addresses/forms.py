from django import forms
from . import models
from django_countries import Countries
from django_countries.widgets import CountrySelectWidget

class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = ('recipient_name', 'street_address', 'municipality', 'region',
            'postal_code', 'country',
        )
        labels = {
            'recipient_name': 'Recipient',
            'street_address': 'Address',
            'municipality':   'City/Town',
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

    def clean(self):
        self.cleaned_data = super(AddressForm, self).clean()

        country = self.cleaned_data.get('country')
        postal_code = self.cleaned_data.get('postal_code')

        if country and country != 'IE' and not postal_code:
            label = self.fields['postal_code'].label
            country_name = Countries().name(country)
            error_message = (
                ('The %s field is required for addresses within the selected '
                 'country (%s).') % (label, country_name)
            )
            self.add_error('postal_code', error_message)
        elif country == 'IE' and postal_code:
            self.cleaned_data.update({
                'postal_code': None,
            })

        return self.cleaned_data
