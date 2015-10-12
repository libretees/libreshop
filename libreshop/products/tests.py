from django.test import TestCase
from .models import Product, Variant, Component

# Create your tests here.
class ProductModelTest(TestCase):

    def test_model_has_sku_field(self):
        '''
        Tests that Product.sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = getattr(product, 'sku', None)
        self.assertIsNotNone(sku)


    def test_model_has_name_field(self):
        '''
        Tests that Product.name is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = getattr(product, 'name', None)
        self.assertIsNotNone(sku)


    def test_saving_and_retrieving_products_from_the_database(self):
        '''
        Tests that a Product can be successfuly saved to the database.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_products = Product.objects.all().count()
        self.assertEqual(num_products, 1)


    def test_creating_exactly_one_variant_alongside_product(self):
        '''
        Tests that a Variant is created on the `many` side of the mandatory
        1-to-many relationship between Products and Variants.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_variants = Variant.objects.all().count()
        self.assertEqual(num_variants, 1)


    def test_creating_exactly_one_component_alongside_product(self):
        '''
        Tests that a Component is created on the `many` side of the mandatory
        1-to-many relationship between Variants and Components.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_components = Component.objects.all().count()
        self.assertEqual(num_components, 1)


    def test_single_variant_has_same_name_as_parent_product_at_creation(self):
        '''
        Tests that a single child Variant inherits the name of its parent
        Product.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variants = Variant.objects.filter(product=product)
        variant = variants[0] if variants else None
        self.assertEqual(product.name, variant.name)


    def test_single_variant_has_same_name_as_parent_product_at_variant_update(self):
        '''
        Tests that a single child Variant cannot change its name from the name
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
        Tests that a child Variant with siblings takes the name of its parent
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
        Tests that a child Variant takes the name of its parent Product when the
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
        Tests that a sibling Variant can change its name.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        self.assertNotEqual(variant1.name, variant2.name)


    def test_original_variant_can_be_renamed_when_sibling_present(self):
        '''
        Tests that the first child Variant can change its name, when siblings
        are present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        variant1.name = 'bar'
        variant1.save()
        variant1.refresh_from_db()
        self.assertEqual(variant1.name, 'bar')

    def test_original_variant_is_not_renamed_when_sibling_present_at_product_update(self):
        '''
        Tests that the first child Variant does not inherit its parents name
        after a sibling is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant1 = Variant.objects.filter(product=product)[0]
        variant2 = Variant.objects.create(name='baz', product=product)
        product.name = 'bar'
        product.save()
        product.refresh_from_db()
        self.assertEqual(variant1.name, 'foo')

    def test_sibling_variant_is_not_renamed_when_sibling_present_at_product_update(self):
        '''
        Tests that the first child Variant does not inherit its parents name
        after a sibling is present.
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
        Tests that Variant.product is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        product = getattr(variant, 'product', None)
        self.assertIsNotNone(product)


    def test_model_has_product_field(self):
        '''
        Tests that Variant.name is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = getattr(variant, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_product_field(self):
        '''
        Tests that Variant.sub_sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        sub_sku = getattr(variant, 'sub_sku', None)
        self.assertIsNotNone(sub_sku)


    def test_model_has_product_field(self):
        '''
        Tests that Variant.price is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = getattr(variant, 'price', None)
        self.assertIsNotNone(price)


    def test_saving_and_retrieving_variants_from_the_database(self):
        '''
        Tests that a Variant can be successfuly saved to the database.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant(product=product, name='bar')
        variant.save()
        num_variants = Variant.objects.all().count()
        self.assertEqual(num_variants, 1)
