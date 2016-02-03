from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory
from django.test import TestCase
from .forms.models import UniqueTogetherFormSet
from .models import Inventory, Location, Warehouse

# Create your tests here.
class UniqueTogetherFormSetTest(TestCase):

    def setUp(self):
        self.post_data = {
            'location_set-INITIAL_FORMS': '0',
            'location_set-TOTAL_FORMS': '2',
            'location_set-0-id': '',
            'location_set-0-inventory': '',
            'location_set-0-quantity': '',
            # 'location_set-0-warehouse': '1',
            'location_set-1-id': '',
            'location_set-1-inventory': '',
            'location_set-1-quantity': '',
            # 'location_set-1-warehouse': '1',
        }


    def test_formset_raises_exception_for_duplicate_values_in_intermediate_model(self):
        '''
        Test that UniqueTogetherFormSet raises an exception when duplicate
        values exist for an intermediate model's Meta.unique_together field.
        '''
        warehouse = Warehouse.objects.create(name='foo')

        self.post_data.update({
            'location_set-0-warehouse': warehouse.pk,
            'location_set-1-warehouse': warehouse.pk,
        })

        FormSet = inlineformset_factory(
            Inventory, Location, formset=UniqueTogetherFormSet,
            fields=('inventory', 'warehouse')
        )

        formset = FormSet(data=self.post_data)

        self.assertRaises(ValidationError, formset.clean)


    def test_formset_is_valid_for_unique_values(self):
        '''
        Test that UniqueTogetherFormSet is valid when no duplicate values exist
        for an intermediate model's Meta.unique_together field.
        '''
        warehouse1 = Warehouse.objects.create(name='foo')
        warehouse2 = Warehouse.objects.create(name='bar')

        self.post_data.update({
            'location_set-0-warehouse': warehouse1.pk,
            'location_set-1-warehouse': warehouse2.pk,
        })

        FormSet = inlineformset_factory(
            Inventory, Location, formset=UniqueTogetherFormSet,
            fields=('inventory', 'warehouse')
        )

        formset = FormSet(data=self.post_data)

        self.assertTrue(formset.is_valid())


    def test_formset_is_invalid_for_duplicate_values(self):
        '''
        Test that UniqueTogetherFormSet is invalid when duplicate values exist
        for an intermediate model's Meta.unique_together field.
        '''
        warehouse = Warehouse.objects.create(name='foo')

        self.post_data.update({
            'location_set-0-warehouse': warehouse.pk,
            'location_set-1-warehouse': warehouse.pk,
        })

        FormSet = inlineformset_factory(
            Inventory, Location, formset=UniqueTogetherFormSet,
            fields=('inventory', 'warehouse')
        )

        formset = FormSet(data=self.post_data)

        self.assertFalse(formset.is_valid())
