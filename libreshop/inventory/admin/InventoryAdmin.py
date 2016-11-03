# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from common.forms import UniqueTogetherFormSet
from ..forms import InventoryCreationForm
from ..models import Location

# Initialize logger
logger = logging.getLogger(__name__)

class LocationTabularInline(admin.TabularInline):
    model = Location
    formset = UniqueTogetherFormSet
    min_num = 1
    extra = 0

class InventoryAdmin(admin.ModelAdmin):
    form = InventoryCreationForm
    inlines = [LocationTabularInline]
