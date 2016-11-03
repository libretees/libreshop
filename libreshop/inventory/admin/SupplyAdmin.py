# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from .models import Supply

# Initialize logger
logger = logging.getLogger(__name__)

class SupplyAdmin(admin.TabularInline):
    model = Supply
    exclude = ['landed_cost', 'units_received']
    min_num = 1
    extra = 0
