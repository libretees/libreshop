from decimal import Decimal
from django.test import TestCase
from braintree.validation_error import ValidationError
from ..forms import PaymentForm
try:
    # Try to import from the Python 3.3+ standard library.
    from unittest.mock import patch
except ImportError as e:
    # Otherwise, import from the `mock` project dependency.
    from mock import patch

# Create your tests here.
class PaymentFormTest(TestCase):

    def test_form_is_pci_compliant(self):
        '''
        Test that the Form is PCI Compliant and does not send any sensitive data
        to the server in its POST request.
        '''
        # Instantiate Form.
        form = PaymentForm()

        self.assertNotIn(' name=', str(form))


    def test_form_is_valid_when_provided_with_valid_nonce(self):
        '''
        Test that the Form is valid when a nonce is received from the user on
        behalf of the Payment Gateway and subsequently processed.
        '''
        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(1.00),   # Set Test Amount to 'Authorized'.
            data={
                'payment_method_nonce': 'fake-valid-nonce'
            }
        )
        # Perform Form validation.
        result = form.is_valid()

        self.assertTrue(result)


    def test_form_is_invalid_when_no_nonce_is_provided(self):
        '''
        Test that the Form is invalid when no nonce is received from the user.
        This could happen if the Payment Processor's JavaScript Client is not
        loaded.
        '''
        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(1.00),   # Set Test Amount to 'Authorized'.
            data={
                'payment_method_nonce': None
            }
        )
        # Perform Form validation.
        result = form.is_valid()

        self.assertFalse(result)


    def test_form_does_not_submit_transaction_for_zero_amount(self):
        '''
        Test that the form does not submit a transaction to the Payment Gateway
        if the payment amount is zero.
        '''
        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(0.00),
            data={
                'payment_method_nonce': 'fake-valid-nonce'
            }
        )
        # Perform Form validation.
        result = form.is_valid()

        self.assertNotIn('transaction_id', form.cleaned_data)


    def test_form_is_invalid_when_processor_declines_payment(self):
        '''
        Test that the Form is invalid when the Payment Gateway declines payment.
        '''
        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(2000.00), # Set Test Amount to 'Processor Declined'.
            data={
                'payment_method_nonce': 'fake-valid-nonce'
            }
        )

        # Perform Form validation.
        result = form.is_valid()

        self.assertFalse(result)


    @patch('orders.forms.braintree.Transaction.sale')
    def test_form_is_invalid_when_postal_code_is_missing(self, sale_mock):
        '''
        Test that the Form is invalid when no postal code is entered by the
        user.
        '''
        # Mock error returned by the Payment Gateway.
        error = ValidationError(attributes={
            'code': '81801',
            'attribute': 'base',
            'message': 'Addresses must have at least one field filled in.'
        })
        sale_mock.return_value.is_success = False
        sale_mock.return_value.errors.deep_errors = [error]

        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(1.00), # Set Test Amount to 'Authorized'.
            data={
                'payment_method_nonce': 'fake-valid-nonce'
            }
        )

        # Perform Form validation.
        result = form.is_valid()

        self.assertFalse(result)


    @patch('orders.forms.braintree.Transaction.sale')
    def test_form_is_invalid_when_credit_card_information_is_missing(self, sale_mock):
        '''
        Test that the form is invalid when no credit card information is entered
        by the user.
        '''
        # Mock errors returned by the Payment Gateway.
        error = ValidationError(attributes={
            'code': '91569',
            'attribute': 'payment_method_nonce',
            'message': (
                'payment_method_nonce does not contain a valid payment '
                'instrument type.'
            )
        })
        error2 = ValidationError(attributes={
            'code': '81714',
            'attribute': 'number',
            'message': 'Credit card number is required.'
        })
        error3 = ValidationError(attributes={
            'code': '81725',
            'attribute': 'base',
            'message': (
                'Credit card must include number, payment_method_nonce, or '
                'venmo_sdk_payment_method_code.'
            )
        })
        error4 = ValidationError(attributes={
            'code': '81706',
            'attribute': 'cvv',
            'message': 'CVV is required.'
        })
        sale_mock.return_value.is_success = False
        sale_mock.return_value.errors.deep_errors = [
            error, error2, error3, error4
        ]

        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(1.00), # Set Test Amount to 'Authorized'.
            data={
                'payment_method_nonce': 'fake-valid-nonce'
            }
        )

        # Perform Form validation.
        result = form.is_valid()

        self.assertFalse(result)


    @patch('orders.forms.braintree.Transaction.sale')
    def test_form_is_invalid_when_payment_gateway_responds_with_error(self, sale_mock):
        '''
        Test that the Form is invalid when the Payment Gateway returns any type
        of error.
        '''
        # Mock error returned by the Payment Gateway.
        error = ValidationError(attributes={
            'code': '12345',
            'attribute': 'foo',
            'message': 'This is a generic test error.'
        })
        sale_mock.return_value.is_success = False
        sale_mock.return_value.errors.deep_errors = [error]

        # Instantiate Form.
        form = PaymentForm(
            amount=Decimal(1.00), # Set Test Amount to 'Authorized'.
            data={
                'payment_method_nonce': 'fake-valid-nonce'
            }
        )

        # Perform Form validation.
        result = form.is_valid()

        self.assertFalse(result)
