import logging
import braintree
from datetime import date
from django import forms
from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import Count
from django.template import Context, Engine
from .models import Communication, Order, Transaction

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
        cleaned_data = super(PaymentForm, self).clean()

        if self.amount and not self.errors:
            result = self.create_transaction(self.amount)
            if result.is_success:
                transaction = result.transaction
                payment_card = transaction.credit_card
                cleaned_data.update({
                    'transaction_id': transaction.id,
                    'amount': transaction.amount,
                    'cardholder_name': payment_card['cardholder_name'],
                    'country': payment_card['customer_location'],
                    'payment_card_type': payment_card['card_type'],
                    'payment_card_last_4': payment_card['last_4'],
                    'payment_card_expiration_date': (
                        '%s/%s' % (
                            payment_card['expiration_month'],
                            payment_card['expiration_year'][-2:]
                        )
                    ),
                    'created_at': transaction.created_at,
                    'authorized': result.is_success
                })

        return cleaned_data


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


class OrderReceiptForm(forms.Form):

    template_name = 'orders/email_receipt.html'

    email_address = forms.EmailField(label='email address', required=True)
    next = forms.CharField(label='next URL', required=False)

    def __init__(self, *args, **kwargs):
        from .views import UUID

        self.request = kwargs.pop('request', None)

        super(OrderReceiptForm, self).__init__(*args, **kwargs)

        if self.is_bound:
            session_data = self.request.session.get(UUID)
            if session_data and 'email_address' in session_data:
                del session_data['email_address']
                self.request.session.modified = True

        for field in self.fields.values():
            if field.required:
                field.error_messages.update({
                    'required': 'Your %s is required.' % field.label,
                })


    def clean(self):
        from .views import UUID

        self.cleaned_data = super(OrderReceiptForm, self).clean()

        if self.is_bound and not self.errors:

            session_data = (
                self.request.session.get(UUID) if self.request else None
            )
            self.order_token = (
                session_data.get('order_token') if session_data else None
            )

            abuse = self.prevent_abuse()

            if not abuse:

                email_sent = self.send_email()

                if not email_sent:
                    self.add_error(
                        None,
                        'There was a problem sending the receipt.'
                    )
                else:
                    session_data.update({
                        'email_address': self.cleaned_data.get('email_address'),
                    })
                    self.request.session.modified = True

        return self.cleaned_data


    def prevent_abuse(self):

        abuse = False

        to_email = self.cleaned_data['email_address']

        email_recipients = (
            Communication.objects.filter(
                order__token=self.order_token
            ).values('to_email').annotate(total_sent=Count('to_email'))
        )

        email_addresses = [
            recipient['to_email'] for recipient in email_recipients
        ]

        if email_recipients.count() >= 3 and to_email not in email_addresses:
            abuse = True
            self.add_error(
                None,
                'You cannot send a receipt to more than 3 email addresses.'
            )

        spam_recipients = [
            recipient['to_email'] for recipient in email_recipients
            if recipient['to_email'] == to_email
            and recipient['total_sent'] >= 3
        ]

        for recipient in spam_recipients:
            abuse = True
            self.add_error(
                None, 'You cannot send more than 3 receipts to %s.' % recipient
            )

        return abuse


    def send_email(self):
        from .views import UUID

        messages_sent, body = None, None
        if self.is_valid() and self.order_token:

            email_address = self.cleaned_data['email_address']

            subject = 'Your Receipt for LibreShop Order %s!' % self.order_token

            try:
                # Get Order from specified token.
                order = Order.objects.get(token=self.order_token)

                # Get the latest Transaction.
                transaction = Transaction.objects.filter(order=order).latest()
            except (Order.DoesNotExist, Transaction.DoesNotExist) as e:
                pass
            else:
                # Load the default template engine.
                TemplateEngine = Engine.get_default()

                # Render a context to the template specified in `template_name`.
                template = TemplateEngine.get_template(self.template_name)
                context = Context({
                    'order': order,
                    'purchases': order.purchases.all(),
                    'transaction': transaction
                })
                body = template.render(context)

                message = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email_address],
                    bcc=[],
                    connection=None,
                    attachments=None,
                    headers=None,
                    cc=None,
                    reply_to=None
                )

                messages_sent = message.send()

        if messages_sent:
            Communication.objects.create(
                order=order,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_email=email_address,
                subject=subject,
                body=body
            )

        return bool(messages_sent)
