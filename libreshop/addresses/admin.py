from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'recipient_name', 'street_address', 'locality', 'region', 'postal_code',
        'country')
