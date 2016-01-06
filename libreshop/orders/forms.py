import logging
import braintree
from datetime import date
from django import forms

# Initialize logger.
logger = logging.getLogger(__name__)


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
    number = forms.CharField(label='Card number',
                             widget=SensitiveTextInput(attrs={
                                 'autocomplete': 'off'
                             })
    )
    cvv = forms.CharField(label='CVV',
                          min_length=3,
                          max_length=4,
                          widget=SensitiveTextInput(attrs={
                              'autocomplete': 'off'
                          })
    )
    expiration_month = forms.ChoiceField(choices=EXPIRATION_MONTH_CHOICES,
                                         widget=SensitiveSelectInput()
    )
    expiration_year = forms.ChoiceField(choices=EXPIRATION_YEAR_CHOICES,
                                        widget=SensitiveSelectInput()
    )
    postal_code = forms.CharField(required=True,
                                  widget=SensitiveTextInput()
    )

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        if self.is_bound:
            self.unbound_fields = self.fields
            self.fields = {
                'payment_method_nonce': forms.CharField(required=True)
            }
            self.full_clean()
            self.create_transaction('10.00')


    def create_transaction(self, total):

        # Attempt to create a sales transaction.
        result = braintree.Transaction.sale({
            'amount': total,
            'payment_method_nonce': self.cleaned_data['payment_method_nonce']
        })

        if not result.is_success:
            logger.error('Error response received from Braintree API')

            # Restore unbound fields.
            self.fields = self.unbound_fields

            # Remove duplicate validation errors from the Braintree response.
            errors = result.errors.deep_errors
            errors = [
                error for i, error in enumerate(errors)
                if error.code not in [error.code for error in errors][:i]
            ]

            # Display the validation errors to the user.
            for error in errors:
                if error.attribute in self.fields:
                    self.add_error(error.attribute, error.message)
                elif error.code in ['81801']:
                    self.add_error('postal_code', 'Postal code is required.')
                else:
                    self.add_error(
                        None,
                        (('There was a problem processing your payment!\n'
                          'Error %s: %s') % (error.code, error.message))
                    )
                logger.error(
                    'Error %s: %s (\'%s\' attribute)' %
                    (error.code, error.message, error.attribute)
                )

        return result
