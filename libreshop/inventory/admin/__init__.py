# -*- coding: utf-8 -*-
import logging
from django.contrib import admin
from common.admin import UnindexedAdmin
from .InventoryAdmin import InventoryAdmin
from .PurchaseOrderAdmin import PurchaseOrderAdmin
from .. import models

# Initialize logger.
logger = logging.getLogger(__name__)

# Register your models here.
admin.site.register(models.Inventory, InventoryAdmin)
admin.site.register(models.Location)
admin.site.register(models.PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(models.Supply, UnindexedAdmin)
admin.site.register(models.Warehouse)
