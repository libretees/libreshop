import logging
from decimal import Decimal
from django.test import TestCase
from .models import Product, Variant, Component
from inventory.models import Inventory, Location

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class ProductModelTest(TestCase):

    def test_model_has_sku_field(self):
        '''
        Test that Product.sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = None
        try:
            sku = product._meta.get_field('sku')
        except:
            pass
        self.assertIsNotNone(sku)


    def test_model_sku_field_is_unique(self):
        '''
        Test that Product.sku is unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = None
        try:
            sku = product._meta.get_field('sku')
        except:
            pass
        unique = getattr(sku, 'unique', None)
        self.assertTrue(unique)


    def test_model_sku_field_is_required(self):
        '''
        Test that Product.sku is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = None
        try:
            sku = product._meta.get_field('sku')
        except:
            pass
        nullable = getattr(sku, 'null', None)
        self.assertFalse(nullable)


    def test_model_sku_field_cannot_be_blank(self):
        '''
        Test that Product.sku does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = None
        try:
            sku = product._meta.get_field('sku')
        except:
            pass
        blank = getattr(sku, 'blank', None)
        self.assertFalse(blank)


    def test_model_sku_field_has_max_length(self):
        '''
        Test that Product.sku max length is 8.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = None
        try:
            sku = product._meta.get_field('sku')
        except:
            pass
        max_length = getattr(sku, 'max_length', None)
        self.assertEqual(max_length, 8)


    def test_model_has_name_field(self):
        '''
        Test that Product.name is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        name = None
        try:
            name = product._meta.get_field('name')
        except:
            pass
        self.assertIsNotNone(name)


    def test_model_name_field_is_unique(self):
        '''
        Test that Product.name is unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        name = None
        try:
            name = product._meta.get_field('name')
        except:
            pass
        unique = getattr(name, 'unique', None)
        self.assertTrue(unique)


    def test_model_name_field_is_required(self):
        '''
        Test that Product.name is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        name = None
        try:
            name = product._meta.get_field('name')
        except:
            pass
        nullable = getattr(name, 'null', None)
        self.assertFalse(nullable)


    def test_model_name_field_cannot_be_blank(self):
        '''
        Test that Product.name does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        name = None
        try:
            name = product._meta.get_field('name')
        except:
            pass
        blank = getattr(name, 'blank', None)
        self.assertFalse(blank)


    def test_model_name_field_has_max_length(self):
        '''
        Test that Product.name max length is 64.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        name = None
        try:
            name = product._meta.get_field('name')
        except:
            pass
        max_length = getattr(name, 'max_length', None)
        self.assertEqual(max_length, 64)


    def test_saving_to_and_retrieving_products_from_the_database(self):
        '''
        Test that a Product can be successfuly saved to the database.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_products = Product.objects.all().count()
        self.assertEqual(num_products, 1)


    def test_creating_exactly_one_variant_alongside_product(self):
        '''
        Test that a Variant is created on the `many` side of the mandatory
        1-to-Many relationship between Products and Variants.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_variants = Variant.objects.all().count()
        self.assertEqual(num_variants, 1)


    def test_creating_exactly_one_component_alongside_product(self):
        '''
        Test that a Component is created on the `many` side of the mandatory
        1-to-Many relationship between Variants and Components.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_components = Component.objects.all().count()
        self.assertEqual(num_components, 1)


    def test_single_variant_has_same_name_as_parent_product_at_creation(self):
        '''
        Test that a single child Variant inherits the name of its parent
        Product.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variants = Variant.objects.filter(product=product)
        variant = variants[0] if variants else None
        self.assertEqual(product.name, variant.name)


    def test_single_variant_has_same_name_as_parent_product_at_variant_update(self):
        '''
        Test that a single child Variant cannot change its name from the name
        inherited from its parent Product.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variants = Variant.objects.filter(product=product)
        variant = variants[0] if variants else None
        variant.name = 'bar'
        variant.save()
        self.assertEqual(product.name, variant.name)


    def test_single_variant_has_same_name_as_parent_product_at_sibling_deletion(self):
        '''
        Test that a child Variant with siblings takes the name of its parent
        Product when it becomes an only child.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        variant1.name = 'bar'
        variant1.save()
        variant1.refresh_from_db()
        variant2.delete()
        variant1.refresh_from_db()
        self.assertEqual(variant1.name, 'foo')


    def test_single_variant_has_same_name_as_parent_product_at_product_update(self):
        '''
        Test that a child Variant takes the name of its parent Product when the
        parent changes its name.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variants = Variant.objects.filter(product=product)
        variant = variants[0] if variants else None
        product.name = 'bar'
        product.save()
        variant.refresh_from_db()
        self.assertEqual(product.name, variant.name)


    def test_sibling_variant_can_have_different_name(self):
        '''
        Test that a sibling Variant can change its name.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        self.assertNotEqual(variant1.name, variant2.name)


    def test_original_variant_can_be_renamed_when_sibling_present(self):
        '''
        Test that the first child Variant can change its name, when siblings
        are present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        variant1.name = 'bar'
        variant1.save()
        variant1.refresh_from_db()
        self.assertEqual(variant1.name, 'bar')


    def test_original_variant_is_not_renamed_at_product_update_when_sibling_present(self):
        '''
        Test that the first child Variant does not inherit its parent's name
        when a sibling is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        product.name = 'bar'
        product.save()
        product.refresh_from_db()
        self.assertEqual(variant1.name, 'foo')


    def test_sibling_variant_is_not_renamed_at_product_update_when_sibling_present(self):
        '''
        Test that any subsequent child Variants do not inherit their parent's
        name when a sibling is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        product.name = 'bar'
        product.save()
        product.refresh_from_db()
        self.assertEqual(variant2.name, 'baz')


class VariantModelTest(TestCase):

    def test_model_has_product_field(self):
        '''
        Test that Variant.product is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        product = None
        try:
            product = variant._meta.get_field('product')
        except:
            pass
        self.assertIsNotNone(product)


    def test_model_product_field_is_not_unique(self):
        '''
        Test that Variant.product is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        product = None
        try:
            product = variant._meta.get_field('product')
        except:
            pass
        unique = getattr(product, 'unique', None)
        self.assertFalse(unique)


    def test_model_product_field_is_required(self):
        '''
        Test that Variant.product is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        product = None
        try:
            product = variant._meta.get_field('product')
        except:
            pass
        nullable = getattr(product, 'null', None)
        self.assertFalse(nullable)


    def test_model_product_field_cannot_be_blank(self):
        '''
        Test that Variant.product does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        product = None
        try:
            product = variant._meta.get_field('product')
        except:
            pass
        blank = getattr(product, 'blank', None)
        self.assertFalse(blank)


    def test_model_has_name_field(self):
        '''
        Test that Variant.name is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = None
        try:
            name = variant._meta.get_field('name')
        except:
            pass
        self.assertIsNotNone(name)


    def test_model_name_field_is_not_unique(self):
        '''
        Test that Variant.name is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = None
        try:
            name = variant._meta.get_field('name')
        except:
            pass
        unique = getattr(name, 'unique', None)
        self.assertFalse(unique)


    def test_model_name_field_is_required(self):
        '''
        Test that Variant.name is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = None
        try:
            name = variant._meta.get_field('name')
        except:
            pass
        nullable = getattr(name, 'null', None)
        self.assertFalse(nullable)


    def test_model_name_field_cannot_be_blank(self):
        '''
        Test that Variant.name does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = None
        try:
            name = variant._meta.get_field('name')
        except:
            pass
        blank = getattr(name, 'blank', None)
        self.assertFalse(blank)


    def test_model_name_field_has_max_length(self):
        '''
        Test that Variant.name max length is 64.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = None
        try:
            name = variant._meta.get_field('name')
        except:
            pass
        max_length = getattr(name, 'max_length', None)
        self.assertEqual(max_length, 64)


    def test_model_name_field_max_length_is_equal_to_product_max_length(self):
        '''
        Test that Variant.name and Product.name have an equal max length value.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        product_name = None
        variant_name = None
        try:
            product_name = product._meta.get_field('name')
            variant_name = variant._meta.get_field('name')
        except:
            pass
        product_name_max_length = getattr(product_name, 'max_length', 0)
        variant_name_max_length = getattr(variant_name, 'max_length', 0)
        self.assertEqual(product_name_max_length, variant_name_max_length)


    def test_model_has_sub_sku_field(self):
        '''
        Test that Variant.sub_sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        self.assertIsNotNone(sub_sku)


    def test_model_sub_sku_field_is_not_unique(self):
        '''
        Test that Variant.sub_sku is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        unique = getattr(sub_sku, 'unique', None)
        self.assertFalse(unique)


    def test_model_product_and_sub_sku_fields_are_unique_together(self):
        '''
        Test that Variant.product and Variant.sub_sku are unique together.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        unique_together = getattr(variant._meta, 'unique_together', None)
        self.assertIn(('product', 'sub_sku'), unique_together)


    def test_model_sub_sku_field_is_required(self):
        '''
        Test that Variant.sub_sku is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        nullable = getattr(sub_sku, 'null', None)
        self.assertFalse(nullable)


    def test_model_sub_sku_field_cannot_be_blank(self):
        '''
        Test that Variant.sub_sku does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        blank = getattr(sub_sku, 'blank', None)
        self.assertFalse(blank)


    def test_model_sub_sku_field_has_max_length(self):
        '''
        Test that Variant.sub_sku max length is 8.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        max_length = getattr(sub_sku, 'max_length', None)
        self.assertEqual(max_length, 8)


    def test_model_has_price_field(self):
        '''
        Test that Variant.price is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        self.assertIsNotNone(price)


    def test_model_price_field_is_not_unique(self):
        '''
        Test that Variant.price is not unique.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        unique = getattr(price, 'unique', None)
        self.assertFalse(unique)


    def test_model_price_field_is_required(self):
        '''
        Test that Variant.price is required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        nullable = getattr(price, 'null', None)
        self.assertFalse(nullable)


    def test_model_price_field_cannot_be_blank(self):
        '''
        Test that Variant.price does not allow blank values in forms.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        blank = getattr(price, 'blank', None)
        self.assertFalse(blank)


    def test_model_price_field_has_default(self):
        '''
        Test that Variant.price has a default value of 0.00.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        default = getattr(price, 'default', None)
        self.assertEqual(default, Decimal(0.00))


    def test_model_price_field_max_digits(self):
        '''
        Test that Variant.price will allow 8 digits, at maximum.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        max_digits = getattr(price, 'max_digits', None)
        self.assertEqual(max_digits, 8)


    def test_model_price_field_decimal_places(self):
        '''
        Test that Variant.price will allow 2 decimal places, at maximum.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = None
        try:
            price = variant._meta.get_field('price')
        except:
            pass
        decimal_places = getattr(price, 'decimal_places', None)
        self.assertEqual(decimal_places, 2)


    def test_saving_to_and_retrieving_variants_from_the_database(self):
        '''
        Test that a Variant can be successfuly saved to the database.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant(product=product, name='bar')
        variant.save()
        num_variants = Variant.objects.filter(name='bar').count()
        self.assertEqual(num_variants, 1)


    def test_new_variant_is_created_when_parents_only_child_is_deleted(self):
        '''
        Test that a new Variant is created when the only child to the parent
        Product is deleted.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.filter(product=product)[0]
        original_variant_id = variant.id
        variant.delete()
        variant = Variant.objects.filter(product=product)[0]
        self.assertNotEqual(original_variant_id, variant.id)


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


    def test_model_inventory_field_is_required(self):
        '''
        Test that Component.inventory is required.
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
        self.assertFalse(nullable)


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


    def test_new_component_is_created_when_parents_only_child_is_deleted(self):
        '''
        Test that a new Component is created when the only child to the parent
        Variant is deleted.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(product=product, name='bar')
        component = Component.objects.filter(variant=variant)[0]
        original_component_id = component.id
        component.delete()
        component = Component.objects.filter(variant=variant)[0]
        self.assertNotEqual(original_component_id, component.id)
