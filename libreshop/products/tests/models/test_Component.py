import logging
from decimal import Decimal
from django.test import TestCase
from inventory.models import Inventory
from ...models import Attribute, AttributeValue, Product, Variant, Component

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class ComponentModelTest(TestCase):

    def test_model_has_variant_field(self):
        '''
        Test that Component.variant is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        variant = None
        try:
            variant = component._meta.get_field('variant')
        except:
            pass
        self.assertIsNotNone(variant)


    def test_model_variant_field_is_not_unique(self):
        '''
        Test that Component.variant is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        variant = None
        try:
            variant = component._meta.get_field('variant')
        except:
            pass
        unique = getattr(variant, 'unique', None)
        self.assertFalse(unique)


    def test_model_variant_and_inventory_fields_are_unique_together(self):
        '''
        Test that Component.variant and Component.inventory are unique together.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        unique_together = getattr(component._meta, 'unique_together', None)
        self.assertIn(('variant', 'inventory'), unique_together)


    def test_model_variant_field_is_required(self):
        '''
        Test that Component.variant is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        variant = None
        try:
            variant = component._meta.get_field('variant')
        except:
            pass
        nullable = getattr(variant, 'null', None)
        self.assertFalse(nullable)


    def test_model_variant_field_cannot_be_blank(self):
        '''
        Test that Component.variant does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        variant = None
        try:
            variant = component._meta.get_field('variant')
        except:
            pass
        blank = getattr(variant, 'blank', None)
        self.assertFalse(blank)


    def test_model_has_inventory_field(self):
        '''
        Test that Component.inventory is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        inventory = None
        try:
            inventory = component._meta.get_field('inventory')
        except:
            pass
        self.assertIsNotNone(inventory)


    def test_model_inventory_field_is_not_unique(self):
        '''
        Test that Component.inventory is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        inventory = None
        try:
            inventory = component._meta.get_field('inventory')
        except:
            pass
        unique = getattr(inventory, 'unique', None)
        self.assertFalse(unique)


    def test_model_inventory_field_is_not_required(self):
        '''
        Test that Component.inventory is not required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        inventory = None
        try:
            inventory = component._meta.get_field('inventory')
        except:
            pass
        nullable = getattr(inventory, 'null', None)
        self.assertTrue(nullable)


    def test_model_inventory_field_cannot_be_blank(self):
        '''
        Test that Component.inventory does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        inventory = None
        try:
            inventory = component._meta.get_field('inventory')
        except:
            pass
        blank = getattr(inventory, 'blank', None)
        self.assertFalse(blank)


    def test_model_has_quantity_field(self):
        '''
        Test that Component.quantity is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        self.assertIsNotNone(quantity)


    def test_model_quantity_field_is_not_unique(self):
        '''
        Test that Component.quantity is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        unique = getattr(quantity, 'unique', None)
        self.assertFalse(unique)


    def test_model_quantity_field_is_required(self):
        '''
        Test that Component.quantity is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        nullable = getattr(quantity, 'null', None)
        self.assertFalse(nullable)


    def test_model_quantity_field_cannot_be_blank(self):
        '''
        Test that Component.quantity does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        blank = getattr(quantity, 'blank', None)
        self.assertFalse(blank)


    def test_model_quantity_field_has_default(self):
        '''
        Test that Component.quantity has a default value of 0.00.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        default = getattr(quantity, 'default', None)
        self.assertEqual(default, Decimal(0.00))


    def test_model_quantity_field_max_digits(self):
        '''
        Test that Component.quantity will allow 8 digits, at maximum.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        max_digits = getattr(quantity, 'max_digits', None)
        self.assertEqual(max_digits, 8)


    def test_model_quantity_field_decimal_places(self):
        '''
        Test that Component.quantity will allow 2 decimal places, at maximum.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = None
        try:
            quantity = component._meta.get_field('quantity')
        except:
            pass
        decimal_places = getattr(quantity, 'decimal_places', None)
        self.assertEqual(decimal_places, 2)


    def test_saving_to_and_retrieving_components_from_the_database(self):
        '''
        Test that a Component can be successfuly saved to the database.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(product=product, name='bar')
        component = Component(variant=variant, quantity=Decimal(1.00))
        component.save()
        num_components = (Component.objects.filter(quantity=Decimal(1.00)).
            count())
        self.assertEqual(num_components, 1)


    def test_invalid_child_component_is_deleted_when_valid_child_component_is_created(self):
        '''
        Test that invalid child Components are deleted when a valid child
        Component is created.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.filter(product=product)[0]
        inventory = Inventory.objects.create(name='baz')
        component = Component.objects.create(variant=variant,
            inventory=inventory, quantity=Decimal(1.00))
        num_components = Component.objects.filter(variant=variant).count()
        self.assertEqual(num_components, 1)


    def test_invalid_child_component_is_deleted_when_valid_child_component_is_saved(self):
        '''
        Test that invalid child Components are deleted when a valid child
        Component is saved.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.filter(product=product)[0]
        inventory = Inventory.objects.create(name='baz')
        component = Component(variant=variant, inventory=inventory,
            quantity=Decimal(1.00))
        component.save()
        num_components = Component.objects.filter(variant=variant).count()
        self.assertEqual(num_components, 1)
