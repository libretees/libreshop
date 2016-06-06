
from django.contrib import admin

from .models import Alert

# Register your models here.
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    date_hierarchy = 'created'
    list_display = (
        'title', 'expiration', '_active'
    )

    def _active(self, instance):
        return instance.active
    _active.boolean = True # Show Icon instead of 'True'/'False' text.
    _active.admin_order_field = 'active'
