import braintree
from datetime import date
from django import forms


EXPIRATION_MONTH_CHOICES = [(x, x) for x in range(1, 13)]
EXPIRATION_YEAR_CHOICES = [
    (x, x) for x in range(date.today().year, date.today().year + 10)
]


class SensitiveTextInput(forms.TextInput):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(SensitiveTextInput, self).build_attrs(extra_attrs, **kwargs)
        if 'name' in attrs:
            attrs['data-braintree-name'] = attrs['name']
            del attrs['name']
        return attrs


class SensitiveSelectInput(forms.Select):
    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(SensitiveSelectInput, self).build_attrs(extra_attrs, **kwargs)
        if 'name' in attrs:
            attrs['data-braintree-name'] = attrs['name']
            del attrs['name']
        return attrs


class PaymentForm(forms.Form):

    cardholder_name = forms.CharField(required=True,
                                      widget=SensitiveTextInput()
    )
    number = forms.CharField(required=True,
                             label='Card number',
                             widget=SensitiveTextInput(attrs={
                                 'autocomplete': 'off'
                             })
    )
    cvv = forms.CharField(required=True,
                          label='CVV',
                          min_length=3,
                          max_length=4,
                          widget=SensitiveTextInput(attrs={
                              'autocomplete': 'off'
                          })
    )
    expiration_month = forms.ChoiceField(required=True,
                                         choices=EXPIRATION_MONTH_CHOICES,
                                         widget=SensitiveSelectInput()
    )
    expiration_year = forms.ChoiceField(required=True,
                                        choices=EXPIRATION_YEAR_CHOICES,
                                        widget=SensitiveSelectInput()
    )
    postal_code = forms.CharField(required=True,
                                  widget=SensitiveTextInput()
    )

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        if self.is_bound:
            self.fields = {
                'payment_method_nonce': forms.CharField(required=True)
            }

    def create_transaction(self, total):
        result = braintree.Transaction.sale({
            'amount': total,
            'payment_method_nonce': self.cleaned_data['payment_method_nonce']
        })
        return result
