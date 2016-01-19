from django.contrib import admin
from .models import Order, Purchase, TaxRate

# Register your models here.
admin.site.register(Order)
admin.site.register(Purchase)
admin.site.register(TaxRate)
