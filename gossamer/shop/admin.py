from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Product
from .forms import CustomerAdmin

# Register your models here.
admin.site.register(Product)
try:
    admin.site.unregister(get_user_model())
finally:
    admin.site.register(get_user_model(), CustomerAdmin)
