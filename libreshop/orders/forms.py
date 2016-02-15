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


class SensitiveDataMixin(forms.Widget):

    def build_attrs(self, extra_attrs=None, **kwargs):
        attrs = super(SensitiveDataMixin, self).build_attrs(
            extra_attrs, **kwargs
        )
        if 'name' in attrs:
            attrs['data-braintree-name'] = attrs['name']
            del attrs['name']

        return attrs


class SensitiveSelect(SensitiveDataMixin, forms.Select):
    pass

class SensitiveTextInput(SensitiveDataMixin, forms.TextInput):
    pass


class PaymentForm(forms.Form):

    cardholder_name = forms.CharField(
        label='Cardholder Name',
        widget=SensitiveTextInput()
    )
    number = forms.CharField(
        label='Card Number',
        widget=SensitiveTextInput(attrs={
            'autocomplete': 'off'
        })
    )
    cvv = forms.CharField(
        label='CVV',
        min_length=3,
        max_length=4,
        widget=SensitiveTextInput(attrs={
            'autocomplete': 'off'
        })
    )
    expiration_month = forms.ChoiceField(
        label='Expiration Month',
        choices=EXPIRATION_MONTH_CHOICES,
        widget=SensitiveSelect()
    )
    expiration_year = forms.ChoiceField(
        label='Expiration Year',
        choices=EXPIRATION_YEAR_CHOICES,
        widget=SensitiveSelect()
    )
    postal_code = forms.CharField(
        label='ZIP/Postcode/Postal Code',
        widget=SensitiveTextInput()
    )


    def __init__(self, *args, **kwargs):

        self.amount = kwargs.pop('amount', None)

        super(PaymentForm, self).__init__(*args, **kwargs)

        if self.is_bound:
            self.unbound_fields = self.fields
            self.fields = {
                'payment_method_nonce': forms.CharField(required=True)
            }

    def clean(self):
        self.cleaned_data = super(PaymentForm, self).clean()
        if self.amount:
            self.create_transaction(self.amount)
        return self.cleaned_data


    def create_transaction(self, amount):

        # Attempt to create a sales transaction.
        logger.info('Attempting sales transaction...')
        result = braintree.Transaction.sale({
            'amount': amount,
            'payment_method_nonce': self.cleaned_data['payment_method_nonce'],
            'options': {
                'submit_for_settlement': True
            }
        })

        if not result.is_success:
            logger.error('Error response received from Braintree API')

            self.add_error(
                None,
                ('There was a problem processing your payment! Your card was '
                 'not charged. Please correct the errors below and try again.')
            )

            # Restore unbound fields so that error messages can be displayed.
            self.fields = self.unbound_fields

            # Remove duplicate validation errors from the API response.
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
                    # Map Braintree 'base' attribute Error 81801
                    # "Addresses must have at least one field filled in."
                    # to `postal_code` field.
                    self.add_error(
                        'postal_code',
                        'The ZIP/Postcode/Postal Code field is required.'
                    )
                elif error.attribute not in ['base', 'payment_method_nonce']:
                    self.add_error(
                        None,
                        (('There was a problem processing your payment!\n'
                          'Error %s: %s') % (error.code, error.message))
                    )
                logger.error(
                    'Error %s: %s (\'%s\' attribute)' %
                    (error.code, error.message, error.attribute)
                )
        else:
            logger.info('Sales transaction succeeded!')

        return result
