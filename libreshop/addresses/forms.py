from django import forms
from . import models
from django_countries.widgets import CountrySelectWidget

class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = ('recipient_name', 'street_address', 'locality', 'region',
            'postal_code', 'country',
        )
        labels = {
            'recipient_name': 'Recipient',
            'street_address': 'Address',
            'locality': 'City/Town',
            'region': 'State/Province/County',
            'postal_code': 'ZIP/Postcode/Postal Code',
        }
        widgets = {
            'street_address': forms.Textarea(attrs={'rows': 4,}),
            'country': CountrySelectWidget(),
        }

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if field.required:
                field.error_messages.update({
                    'required': 'The %s field is required.' % field.label,
                })
