from django.contrib import admin
from .models import Product, Variant, Component, Inventory, Location, Attribute, Attribute_Value

# Register your models here.
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(Component)
admin.site.register(Inventory)
admin.site.register(Location)
admin.site.register(Attribute)
admin.site.register(Attribute_Value)
