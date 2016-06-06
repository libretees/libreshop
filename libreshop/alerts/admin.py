from django.db.models import DateTimeField, ExpressionWrapper, F
from django.db.models.expressions import Value
from django.contrib import admin
from django.utils import timezone
from .models import Alert

# Register your models here.
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    date_hierarchy = 'created'
    list_display = (
        'title', 'expiration', '_active'
    )

    def _active(self, instance):
        current_time = timezone.now()
        return (instance.expiration or current_time) >= current_time
    _active.boolean = True # Show Icon instead of 'True'/'False' text.
    _active.admin_order_field = 'expiration'
