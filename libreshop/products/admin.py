import logging
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from common.admin import UnindexedAdmin
from fulfillment.admin import FulfillmentSettingValueInline
from . import models
from .forms import (
    PopulatedFormFactory, ProductCreationForm, ProductChangeForm,
    VariantCreationForm
)

# Initialize logger
logger = logging.getLogger(__name__)


class VariantInline(admin.TabularInline):
    model = models.Variant
    fields = ('name', 'sub_sku', 'price')
    extra = 0
    show_change_link = True

    def get_max_num(self, request, obj=None, **kwargs):
        return models.Variant.objects.filter(product=obj).count() if obj else 1


class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'sku')

    form = ProductChangeForm
    add_form = ProductCreationForm


    def get_inline_instances(self, request, obj=None):

        if obj:
            inlines = set(self.inlines)
            inlines = inlines.union({VariantInline,})
            self.inlines = list(inlines)
        else:
            self.inlines = []

        return super(ProductAdmin, self).get_inline_instances(request, obj)


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
        return super(ProductAdmin, self).response_add(
            request, obj, post_url_continue
        )


class AttributeAdmin(admin.TabularInline):

    model = models.Attribute_Value
    extra = 0


class ComponentInline(admin.TabularInline):

    model = models.Component
    extra = 0


class VariantAdmin(UnindexedAdmin, admin.ModelAdmin):

    add_form = VariantCreationForm
    inlines = [AttributeAdmin, ComponentInline, FulfillmentSettingValueInline]

    def __init__(self, *args, **kwargs):
        super(VariantAdmin, self).__init__(*args, **kwargs)


    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = PopulatedFormFactory(
                request, models.Variant, self.add_form
            )
        defaults.update(kwargs)
        return super(VariantAdmin, self).get_form(request, obj, **defaults)


# Register your models here.
admin.site.register(models.Attribute, UnindexedAdmin)
admin.site.register(models.Category)
admin.site.register(models.Component, UnindexedAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Variant, VariantAdmin)
