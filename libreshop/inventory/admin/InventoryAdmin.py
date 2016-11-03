# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from .forms import InventoryCreationForm
from . import LocationAdmin

# Initialize logger
logger = logging.getLogger(__name__)

class InventoryAdmin(admin.ModelAdmin):
    form = InventoryCreationForm
    inlines = [LocationAdmin]
