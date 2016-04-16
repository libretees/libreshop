from importlib import import_module
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase
from ..forms import OrderReceiptForm
from ..models import Order, Transaction
from ..views import UUID

class OrderReceiptFormTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up supplemental test data.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None

        # Set up test data.
        self.request = HttpRequest()
        self.request.session = engine.SessionStore(session_key)
        self.request.session[UUID] = {}


    def test_form_includes_email_input_field(self):
        '''
        Test that the Form renders an email <input> field.
        '''
        form = OrderReceiptForm()
        self.assertRegex(str(form), '<input.* type="email" />')


    def test_form_removes_email_adress_from_session_variable_if_present(self):
        '''
        Test that the Form removes the 'email address' key from the Session, if
        it is present. This is used to provide feedback to the user.
        '''
        self.request.session[UUID]['email_address'] = 'foo@example.com'
        self.request.session.modified = True

        form = OrderReceiptForm(
            request=self.request,
            data={
                'email_address': 'bar@example.com'
            }
        )
        email_address = self.request.session[UUID].get('email_address')

        self.assertIsNone(email_address)


    def test_form_is_invalid_when_no_order_token_specified(self):
        '''
        Test that the Form is invalid when no Order Token is specified within
        Session variables.
        '''
        form = OrderReceiptForm(
            request=self.request,
            data={
                'email_address': 'foo@example.com'
            }
        )
        result = form.is_valid()

        self.assertFalse(result)


    def test_form_is_invalid_when_non_existent_order_token_specified(self):
        '''
        Test that the Form is invalid when an invalid Order Token is specified
        within Session variables.
        '''
        self.request.session[UUID]['order_token'] = 'foo'
        self.request.session.modified = True

        form = OrderReceiptForm(
            request=self.request,
            data={
                'email_address': 'foo@example.com'
            }
        )
        result = form.is_valid()

        self.assertFalse(result)


    def test_form_is_invalid_when_invalid_email_address_specified(self):
        '''
        Test that the Form is invalid when an invalid email address is
        specified.
        '''
        order = Order.objects.create()
        transaction = Transaction.objects.create(
            order=order, transaction_id='foo'
        )
        self.request.session[UUID]['order_token'] = order.token
        self.request.session.modified = True

        form = OrderReceiptForm(
            request=self.request,
            data={
                'email_address': 'foo'
            }
        )

        result = form.is_valid()

        self.assertFalse(result)


    def test_form_is_valid_when_valid_email_address_and_order_specified(self):
        '''
        Test that the form is valid when a valid email address and Order are
        specified within POST data and within Session variables, respectively.
        '''
        order = Order.objects.create()
        transaction = Transaction.objects.create(
            order=order, transaction_id='foo'
        )
        self.request.session[UUID]['order_token'] = order.token
        self.request.session.modified = True

        form = OrderReceiptForm(
            request=self.request,
            data={
                'email_address': 'foo@example.com'
            }
        )
        result = form.is_valid()

        self.assertTrue(result)


    def test_form_prevents_spam_abuse_to_multiple_email_addresses(self):
        '''
        Test that the Form prevents spam to multiple email addresses.
        '''
        order = Order.objects.create()
        transaction = Transaction.objects.create(
            order=order, transaction_id='foo'
        )
        self.request.session[UUID]['order_token'] = order.token
        self.request.session.modified = True

        email_addresses = [
            'foo@example.com', 'bar@example.com', 'baz@example.com',
            'qux@example.com'
        ]

        form, results = None, list()
        for email_address in email_addresses:
            form = OrderReceiptForm(
                request=self.request,
                data={
                    'email_address': email_address
                }
            )
            is_valid = form.is_valid()
            results.append(is_valid)

        result = all(result for result in results)

        self.assertFalse(result)


    def test_form_prevents_spam_abuse_to_same_email_address(self):
        '''
        Test that the Form prevents spam to a single email addresses.
        '''
        order = Order.objects.create()
        transaction = Transaction.objects.create(
            order=order, transaction_id='foo'
        )
        self.request.session[UUID]['order_token'] = order.token
        self.request.session.modified = True

        form, results = None, list()
        for i in range(4):
            form = OrderReceiptForm(
                request=self.request,
                data={
                    'email_address': 'foo@example.com'
                }
            )
            is_valid = form.is_valid()
            results.append(is_valid)

        result = all(result for result in results)

        self.assertFalse(result)
