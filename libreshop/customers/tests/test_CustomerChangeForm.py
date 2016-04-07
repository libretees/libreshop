from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from carts.models import Cart
from customers.models import Customer
from products.models import Product, Variant
from ..forms import CustomerChangeForm

User = get_user_model()

# Create your tests here.
class CustomerChangeFormTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user', password=make_password('user')
        )
        self.product = Product.objects.create(sku='foo', name='foo')
        self.variant = Variant.objects.create(
            product=self.product, name='bar', sub_sku='bar'
        )
        self.variant2 = Variant.objects.create(
            product=self.product, name='baz', sub_sku='baz'
        )
        self.customer = Customer.objects.get(user=self.user)


    def test_form_loads_cart_contents(self):
        '''
        Test that CustomerChangeForm loads Variants that are present within a
        Customer's cart.
        '''
        Cart.objects.create(customer=self.customer, variant=self.variant)

        form = CustomerChangeForm(instance=self.user)
        selected_variants = form.initial.get('selected_variants')

        self.assertEqual(selected_variants, [self.variant])


    def test_form_adds_newly_selected_variants(self):
        '''
        Test that CustomerChangeForm adds newly-selected Variants to a
        Customer's cart.
        '''
        Cart.objects.create(customer=self.customer, variant=self.variant)

        form = CustomerChangeForm(instance=self.user)
        form.cleaned_data = {
            'selected_variants': [self.variant, self.variant2]
        }
        form.save()

        cart_contents = [
            customer_cart.variant for customer_cart
            in Cart.objects.filter(customer__user=self.user)
        ]

        self.assertEqual(cart_contents, [self.variant, self.variant2])


    def test_form_removes_unselected_variants(self):
        '''
        Test that CustomerChangeForm removes unselected Variants from a
        Customer's cart.
        '''
        Cart.objects.create(customer=self.customer, variant=self.variant)
        Cart.objects.create(customer=self.customer, variant=self.variant2)

        form = CustomerChangeForm(instance=self.user)
        form.cleaned_data = {
            'selected_variants': [self.variant]
        }
        form.save()

        cart_contents = [
            customer_cart.variant for customer_cart
            in Cart.objects.filter(customer__user=self.user)
        ]

        self.assertEqual(cart_contents, [self.variant])
