from django.contrib import admin
from .models import Purchase, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Purchase)
