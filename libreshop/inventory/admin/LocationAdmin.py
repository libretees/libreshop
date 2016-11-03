# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from common.forms import UniqueTogetherFormSet
from .models import Location

# Initialize logger
logger = logging.getLogger(__name__)

class LocationAdmin(admin.TabularInline):
    model = Location
    formset = UniqueTogetherFormSet
    min_num = 1
    extra = 0
