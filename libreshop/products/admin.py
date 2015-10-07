import types
import logging
from django.contrib import admin
from django.contrib.admin.options import IS_POPUP_VAR
from django import forms
from django.forms.widgets import Select
from .models import Product, Variant, Component, Inventory, Location, Attribute, Attribute_Value
from .forms import ProductCreationForm, ProductChangeForm

# Initialize logger
logger = logging.getLogger(__name__)

# Register your models here.
admin.site.register(Component)
admin.site.register(Inventory)
admin.site.register(Location)
admin.site.register(Attribute)
admin.site.register(Attribute_Value)

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


def VariantFormFactory(request):

    model_field_names = [_.name for _ in Variant._meta.get_fields()]

    class VariantForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(VariantForm, self).__init__(*args, **kwargs)
            if request.method == 'GET':
                # Load initial form fields from GET parameters
                for key in request.GET:
                    try:
                        self.fields[key].required = False
                        self.fields[key].widget.attrs['readonly'] = True
                        self.fields[key].widget.attrs['disabled'] = 'disabled'
                    except KeyError:
                        # Ignore unexpected parameters
                        pass
            else:
                prepopulated_fields = ([name for name in model_field_names
                                          if name in request.GET
                                          and name not in request.POST])
                for name in prepopulated_fields:
                    self.fields[name].required = False

    def get_clean_function(name):
        def func(self):
            return (Product.objects.get(id=request.GET[name])
                if isinstance(self.fields[name], forms.models.ModelChoiceField)
                else request.GET[name])
        return func

    for key in [key for key in request.GET if key in model_field_names]:
        setattr(VariantForm, 'clean_%s' % key, get_clean_function(key))

    return VariantForm


class VariantAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        super(VariantAdmin, self).__init__(*args, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = VariantFormFactory(request)
        defaults.update(kwargs)
        return super(VariantAdmin, self).get_form(request, obj, **defaults)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in request.GET:
            kwargs['queryset'] = Product.objects.filter(id=request.GET[db_field.name])
            kwargs['widget'] = Select(attrs={'disabled': 'disabled'})
            kwargs['required'] = False
        return super(VariantAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Product, ProductAdmin)
admin.site.register(Variant, VariantAdmin)
