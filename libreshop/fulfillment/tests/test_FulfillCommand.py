from django.core.management import BaseCommand, call_command
from django.test import TestCase
from django.utils.six import StringIO
from orders.models import Order, Purchase
from products.models import Product, Variant
from ..management.commands import fulfill

class FulfillCommandLineTest(TestCase):

    def test_command_output_when_no_orders_are_fulfilled(self):
        out = StringIO()
        call_command('fulfill', stdout=out)
        self.assertIn('No orders were fulfilled!', out.getvalue())


    def test_command_output_when_orders_are_fulfilled(self):

        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456'
        )
        order = Order.objects.create()
        purchase = Purchase.objects.create(order=order, variant=variant)

        out = StringIO()
        call_command('fulfill', stdout=out)
        self.assertIn('Fulfilled Order', out.getvalue())
