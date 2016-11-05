from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from orders.models import Order, Purchase, Transaction
from products.models import Product, Variant
from ..views import UUID

class ConfirmationViewTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.product = Product.objects.create(name='foo', sku='123')
        self.variant = Variant.objects.create(
            product=self.product, name='bar', sub_sku='456'
        )
        self.order = Order.objects.create()
        self.purchase = Purchase.objects.create(
            order=self.order, variant=self.variant
        )
        self.transaction = Transaction.objects.create(
            order=self.order, transaction_id='foo'
        )

        # Put Order Token within session variable.
        session = self.client.session
        session.update({
            UUID: {
                'order_token': self.order.token
            }
        })
        session.save()

        self.view_url = reverse('checkout:confirmation')


    def test_view_returns_200_status_if_no_order_token_is_in_session_variables(self):
        '''
        Test that the ConfirmationView returns a 200 OK status if there is no
        Order Token within session variables.
        '''
        session = self.client.session
        del session[UUID]['order_token']
        session.save()

        # Perform test.
        response = self.client.get(self.view_url)
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)


    def test_view_returns_200_status_if_order_token_is_in_session_variables(self):
        '''
        Test that the ConfirmationView returns a 200 OK status if an Order Token
        is present within session variables.
        '''
        # Perform test.
        response = self.client.get(self.view_url)

        self.assertEqual(response.status_code, 200)


    def test_view_redirects_on_successful_post(self):
        '''
        Test that the ConfirmationView returns a 302 Found (Temporary Redirect)
        status if valid Form data is POSTed to the View's OrderReceiptForm.
        '''
        # Set up HTTP POST request.
        request_data = {'email_address': 'test@example.com'}

        # Perform test.
        response = self.client.post(self.view_url, data=request_data, follow=False)

        self.assertRedirects(response, self.view_url)
