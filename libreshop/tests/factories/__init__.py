import factory
from itertools import product
from django.contrib.auth.models import User
from inventory.models import Inventory, Attribute, Attribute_Value
from products.models import Product, Variant


class AdminFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'admin@admin.com'
    username = 'admin'
    password = factory.PostGenerationMethodCall('set_password', 'admin')

    is_superuser = True
    is_staff = True
    is_active = True


class StaffMemberFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'staff@staff.com'
    username = 'staff'
    password = factory.PostGenerationMethodCall('set_password', 'staff')

    is_superuser = False
    is_staff = False
    is_active = True


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'user@user.com'
    username = 'user'
    password = factory.PostGenerationMethodCall('set_password', 'user')

    is_superuser = False
    is_staff = False
    is_active = True


class AttributeValueFactory(factory.DjangoModelFactory):
    class Meta:
        model = Attribute_Value

    value = 'bar'


class AttributeFactory(factory.DjangoModelFactory):
    class Meta:
        model = Attribute

    name = 'foo'


class InventoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Inventory

    name = 'foo'

    @factory.post_generation
    def attr(obj, create, extracted, **kwargs):

        for key in sorted(kwargs):

            attribute = None
            try:
                attribute = Attribute.objects.get(name=key)
            except:
                attribute = AttributeFactory(name=key)

            value = AttributeValueFactory(
                inventory=obj, attribute=attribute, value=kwargs[key]
            )


class VariantFactory(factory.DjangoModelFactory):
    class Meta:
        model = Variant

    name = 'foo'


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    sku = '1000'
    name = 'foo'

    @factory.post_generation
    def salable(obj, create, extracted, **kwargs):
        if extracted:
            inventory = InventoryFactory()
            variant = obj.variant_set.first()
            component = variant.component_set.first()
            component.inventory = inventory
            component.save()


    @factory.post_generation
    def option(obj, create, extracted, **kwargs):
        '''
        Create Product Variants that comply with all specified options. Options
        are declared by through the option__<name> keyword argument in the
        ProductFactory constructor.

        For example, this constructor ensures that 9 Variants are created for
        all combinations of 'foo' and 'bar':
            `ProductFactory(option__foo=[1, 2, 3], option__bar=[4, 5, 6])`
        '''
        # Determine the number of Variants that need to be created.
        num_existing_variants = obj.variant_set.count()
        num_variants_required = 1
        for length in [len(list_) for list_ in kwargs.values()]:
            num_variants_required *= length

        # Create additonal Variants.
        if num_existing_variants < num_variants_required:
            delta = num_variants_required - num_existing_variants
            variants = [VariantFactory(name=obj.name+str(_), product=obj)
                for _ in range(delta)
            ]

        # Calculate all possible combinations of the specified options.
        all_combos = [
            dict(zip(kwargs, combo)) for combo in product(*kwargs.values())
        ]

        # Create an Inventory item for each combination.
        inventory = list()
        for (i, combo) in enumerate(all_combos):
            attributes = {'attr__%s' % key:combo[key] for key in combo}
            inventory.append(InventoryFactory(name=str(i), **attributes))

        # Link Inventory items to Variants and rename Variants.
        variants = obj.variant_set.all()
        for (inventory, variant) in zip(inventory, variants):

            # Link Inventory item to Variant.
            component = variant.component_set.first()
            component.inventory = inventory
            component.save()

            # Rename Variant.
            attribute_values = [
                '/'.join(str(value) for value in values)
                for values in variant.attributes.values()
            ]
            variant.name = '%s (%s)' % (obj.name, ' '.join(attribute_values))
            variant.save()
