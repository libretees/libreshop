from decimal import Decimal
from django.test import TestCase
from .models import Product, Variant, Component
from inventory.models import Inventory, Location

# Create your tests here.
class ProductModelTest(TestCase):

    def test_model_has_sku_field(self):
        '''
        Test that Product.sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = getattr(product, 'sku', None)
        self.assertIsNotNone(sku)


    def test_model_has_name_field(self):
        '''
        Test that Product.name is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        sku = getattr(product, 'name', None)
        self.assertIsNotNone(sku)


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
        1-to-many relationship between Products and Variants.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        num_variants = Variant.objects.all().count()
        self.assertEqual(num_variants, 1)


    def test_creating_exactly_one_component_alongside_product(self):
        '''
        Test that a Component is created on the `many` side of the mandatory
        1-to-many relationship between Variants and Components.
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
        product = getattr(variant, 'product', None)
        self.assertIsNotNone(product)


    def test_model_has_name_field(self):
        '''
        Test that Variant.name is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        name = getattr(variant, 'name', None)
        self.assertIsNotNone(name)


    def test_model_has_sub_sku_field(self):
        '''
        Test that Variant.sub_sku is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', sub_sku='baz',
            product=product)
        sub_sku = getattr(variant, 'sub_sku', None)
        self.assertIsNotNone(sub_sku)


    def test_model_has_price_field(self):
        '''
        Test that Variant.price is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        price = getattr(variant, 'price', None)
        self.assertIsNotNone(price)


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
        variant = getattr(component, 'variant', None)
        self.assertIsNotNone(variant)


    def test_model_has_inventory_field(self):
        '''
        Test that Component.inventory is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        location = Location.objects.create(quantity=Decimal(1.00))
        inventory = Inventory.objects.create(location=inventory_location,
            cost=Decimal(1.00))
        component = Component.objects.create(variant=variant,
            inventory=inventory)
        inventory = getattr(component, 'inventory', None)
        self.assertIsNotNone(inventory)


    def test_model_has_quantity_field(self):
        '''
        Test that Component.quantity is present.
        '''
        product = Product.objects.create(sku='foo', name='foo')
        variant = Variant.objects.create(name='bar', product=product)
        component = Component.objects.create(variant=variant)
        quantity = getattr(component, 'quantity', None)
        self.assertIsNotNone(quantity)


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
