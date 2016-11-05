from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import CustomerAdmin

User = get_user_model()

# Register your models here.
try:
    admin.site.unregister(User)
finally:
    admin.site.register(User, CustomerAdmin)
