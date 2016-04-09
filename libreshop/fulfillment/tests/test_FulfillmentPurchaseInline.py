from decimal import Decimal
from django.contrib.admin import site
from django.http import HttpRequest
from django.test import TestCase
from orders.models import Order, Purchase
from products.models import Product, Variant
from ..admin import FulfillmentPurchaseInline
from ..models import FulfillmentOrder, FulfillmentPurchase


# Create your tests here.
class FulfillmentPurchaseInlineTest(TestCase):

    def setUp(self):
        '''
        Set up test data that would be present for a FulfillmentPurchaseInline.
        '''
        product = Product.objects.create(name='foo', sku='123')
        variant = Variant.objects.create(
            product=product, name='bar', sub_sku='456'
        )
        order = Order.objects.create()
        purchase = Purchase.objects.create(order=order, variant=variant)

        self.fulfillment_order = FulfillmentOrder.objects.create(order_id='foo')
        self.fulfillment_purchase = FulfillmentPurchase.objects.create(
            purchase=purchase, order=self.fulfillment_order
        )


    def test_max_num_equal_to_number_of_child_objects(self):
        '''
        Test that the maximum number of FulfillmentPurchase objects listed in
        the InlineModelAdmin is equal to the number of children to the parent
        FulfillmentOrder.
        '''
        request = HttpRequest()
        admin = FulfillmentPurchaseInline(FulfillmentOrder, site)

        max_num = admin.get_max_num(request, obj=self.fulfillment_order)

        self.assertEqual(max_num, 1)
