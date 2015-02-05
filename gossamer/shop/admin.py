from django.contrib import admin
from shop.models import Product, Cart, Customer

# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Customer)