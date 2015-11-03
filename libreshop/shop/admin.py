from django.contrib import admin
from .models import Address, Purchase, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(Purchase)
