import logging
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from . import models
from .forms import ProductCreationForm, ProductChangeForm, PopulatedFormFactory

# Initialize logger
logger = logging.getLogger(__name__)

# Register your models here.
admin.site.register(models.Component)
admin.site.register(models.Inventory)
admin.site.register(models.Location)
admin.site.register(models.Attribute)
admin.site.register(models.Attribute_Value)

class ProductAdmin(admin.ModelAdmin):

    form = ProductChangeForm
    add_form = ProductCreationForm

    def has_add_permission(self, request):
        """
        Disable 'Add' icon when prepopulating fields.
        """
        if request.method == 'GET' and 'product' in request.GET:
            return False
        else:
            return True

    def has_change_permission(self, request, obj=None):
        """
        Disable 'Edit' icon when prepopulating fields.
        """
        if request.method == 'GET' and 'product' in request.GET:
            return False
        else:
            return True

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during product creation
        """
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(ProductAdmin, self).get_form(request, obj, **defaults)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the Product
        model has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and IS_POPUP_VAR not in request.POST:
            request.POST['_continue'] = 1
        return super(ProductAdmin, self).response_add(request, obj,
                                                      post_url_continue)


class VariantAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(VariantAdmin, self).__init__(*args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = PopulatedFormFactory(models.Variant, request)
        defaults.update(kwargs)
        return super(VariantAdmin, self).get_form(request, obj, **defaults)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variant, VariantAdmin)
