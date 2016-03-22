import logging
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.test import TestCase
from inventory.models import Inventory
from ...models import Attribute, AttributeValue, Product, Variant, Component

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
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


    def test_model_product_and_name_fields_are_unique_together(self):
        '''
        Test that Variant.product and Variant.name are unique together.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        unique_together = getattr(variant._meta, 'unique_together', None)
        self.assertIn(('product', 'name'), unique_together)


    def test_model_product_and_name_fields_are_unique_together_regardless_of_character_case(self):
        '''
        Test that Variant.product and Variant.name are unique together regardless of character case.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        func = Variant.objects.create
        self.assertRaises(ValidationError, func, product=product, name='Foo')


    def test_model_sub_sku_field_and_product_sku_field_are_unique_when_concatenated_together(self):
        '''
        Test that the Product SKU and Variant Sub-SKU are unique at a catalog
        level when they are concatenated together.
        '''
        product1 = Product.objects.create(name='foo', sku='123')
        product2 = Product.objects.create(name='bar', sku='12')
        variant1 = Variant.objects.create(
            product=product1, name='baz', sub_sku='45'
        )
        func = Variant.objects.create
        self.assertRaises(
            ValidationError, func, product=product2, name='baz', sub_sku='345'
        )


    def test_different_products_can_have_same_variant_name(self):
        '''
        Test that two Variants of two distinct Products can have the same
        Variant.name.
        '''
        product1 = Product.objects.create(sku='foo', name='foo')
        product2 = Product.objects.create(sku='bar', name='bar')
        variant1 = Variant.objects.filter(product=product2)[0]
        variant2 = Variant.objects.filter(product=product2)[0]
        variant2.name = 'foo'
        variant2.save()
        variant2.refresh_from_db()
        self.assertEqual(variant1.name, variant2.name)


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


    def test_model_product_and_sub_sku_fields_are_unique_together_regardless_of_character_case(self):
        '''
        Test that Variant.product and Variant.sub_sku are unique together regardless of character case.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.get(product=product)
        variant.sub_sku = 'foo'
        variant.save()
        func = Variant.objects.create
        self.assertRaises(ValidationError, func, product=product, name='bar',
            sub_sku='Foo')


    def test_model_product_and_sub_sku_fields_do_not_invalidate_self_on_subsequent_save(self):
        '''
        Test that Variant.product and Variant.sub_sku does not cause the Variant
        to raise a ValidationError against its own data on a subsequent save.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.get(product=product)
        variant.sub_sku = 'foo'
        variant.save()

        execption_raised = False
        try:
            variant.save()
        except ValidationError as e:
            execption_raised = True

        self.assertFalse(execption_raised)


    def test_different_products_can_have_same_variant_sub_sku(self):
        '''
        Test that two Variants of two distinct Products can have the same
        Variant.sub_sku.
        '''
        product1 = Product.objects.create(sku='foo', name='foo')
        product2 = Product.objects.create(sku='bar', name='bar')
        variant1 = Variant.objects.filter(product=product1)[0]
        variant1.sub_sku = 'baz'
        variant1.save()
        variant1.refresh_from_db()
        variant2 = Variant.objects.filter(product=product2)[0]
        variant2.sub_sku = 'baz'
        variant2.save()
        variant2.refresh_from_db()
        self.assertEqual(variant1.sub_sku, variant2.sub_sku)


    def test_model_sub_sku_field_is_not_required(self):
        '''
        Test that Variant.sub_sku is not required.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        nullable = getattr(sub_sku, 'null', None)
        self.assertTrue(nullable)


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


    def test_model_sub_sku_field_has_verbose_name(self):
        '''
        Test that Variant.sub_sku's verbose name is 'Sub-SKU'.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        verbose_name = getattr(sub_sku, 'verbose_name', None)
        self.assertEqual(verbose_name, 'Sub-SKU')


    def test_model_sub_sku_field_has_verbose_name_plural(self):
        '''
        Test that Variant.sub_sku's plural verbose name is 'Sub-SKUs'.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = None
        try:
            sub_sku = variant._meta.get_field('sub_sku')
        except:
            pass
        verbose_name_plural = getattr(sub_sku, 'verbose_name_plural', None)
        self.assertEqual(verbose_name_plural, 'Sub-SKUs')


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


    def test_model_has_enabled_field(self):
        '''
        Test that Variant.enabled is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        enabled = None
        try:
            enabled = variant._meta.get_field('enabled')
        except:
            pass
        self.assertIsNotNone(enabled)


    def test_model_enabled_field_default(self):
        '''
        Test that Variant.enabled defaults to True.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        enabled = None
        try:
            enabled = variant._meta.get_field('enabled')
        except:
            pass
        enabled = getattr(enabled, 'default', None)
        self.assertTrue(enabled)


    def test_model_has_attributes_property(self):
        '''
        Test that Variant.attributes is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(product=product, name='bar')

        execption_raised = False
        try:
            attributes = variant.attributes
        except AttributeError as e:
            execption_raised = True

        self.assertFalse(execption_raised)


    def test_model_has_sku_property(self):
        '''
        Test that Variant.sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sku = getattr(variant, 'sku', None)
        self.assertIsNotNone(sku)


    def test_sku_property_consists_of_product_sku_and_model_sub_sku(self):
        '''
        Test that Variant.sku consists of the parent Product SKU and the Variant
        Sub-SKU.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(
            name='bar', sub_sku='bar', product=product
        )
        sku = getattr(variant, 'sku', None)
        self.assertEqual(sku, 'foobar')


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
