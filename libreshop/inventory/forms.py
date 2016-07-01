import logging
from django import forms
from .models import Inventory

# Initialize logger
logger = logging.getLogger(__name__)


class InventoryCreationForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'alternatives', 'cost', 'weight')

    def __init__(self, *args, **kwargs):
        super(InventoryCreationForm, self).__init__(*args, **kwargs)
        self.fields['alternatives'].queryset = Inventory.objects.exclude(
            pk=self.instance.pk
        )
