import logging
from django import forms
from django.contrib import admin
from django.db.models.fields.related import ManyToManyRel
from .models import Inventory, Warehouse, Location

# Initialize logger
logger = logging.getLogger(__name__)


class InventoryCreationForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'alternatives', 'cost',)

    def __init__(self, *args, **kwargs):
        super(InventoryCreationForm, self).__init__(*args, **kwargs)
        self.fields['alternatives'].queryset = Inventory.objects.exclude(
            id__exact=self.instance.id)
