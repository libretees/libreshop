import logging
from django.test import TestCase
from ..forms import InventoryCreationForm
from ..models import Inventory

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your tests here.
class InventoryCreationFormTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        # Set up test data.
        self.inventory = Inventory.objects.create(name='foo')
        self.inventory2 = Inventory.objects.create(name='bar')


    def test_form_excludes_self_from_alternatives_field(self):
        '''
        Test that an InventoryCreationForm excludes its own model instance from
        the list of options available in the 'alternatives' field.
        '''
        form = InventoryCreationForm(instance=self.inventory)

        self.assertNotRegex(str(form), '<option value="\d+">foo</option>')


    def test_form_includes_other_instances_in_alternatives_field(self):
        '''
        Test that an InventoryCreationForm includes other model instances in the
        list of options available in the 'alternatives' field.
        '''
        form = InventoryCreationForm(instance=self.inventory)

        self.assertRegex(str(form), '<option value="\d+">bar</option>')
