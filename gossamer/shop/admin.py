from django import forms
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.related import ManyToManyRel
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Product, Cart, Customer

class CustomerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Customer
    
    selected_products = forms.ModelMultipleChoiceField(Product.objects.all()
                                                      ,widget=admin.widgets.FilteredSelectMultiple('Products', False)
                                                      ,required=False)
    
    def __init__(self, *args, **kwargs):
        super(CustomerChangeForm, self).__init__(*args, **kwargs)
        
        if self.instance.pk:
            self.initial['selected_products'] = [customer_cart.product for customer_cart in Cart.objects.filter(customer__pk=self.instance.pk)]
            rel = ManyToManyRel(Product)
            self.fields['selected_products'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['selected_products'].widget, rel, admin.site)
    
    def save(self, *args, **kwargs):
        instance = super(CustomerChangeForm, self).save(*args, **kwargs)

        if instance.pk:
            for selected_product in [customer_cart.product for customer_cart in Cart.objects.filter(customer__pk=self.instance.pk)]:
                if selected_product not in self.cleaned_data['selected_products']:
                    # remove a product that has been unselected
                    customer = Customer.objects.get(pk=instance.pk)
                    Cart.objects.filter(customer__pk=customer.pk, product__pk=selected_product.pk)[0].delete()
                    
            for product in self.cleaned_data['selected_products']:
                if product not in [customer_cart.product for customer_cart in Cart.objects.filter(customer__pk=self.instance.pk)]:
                    # add newly-selected products
                    customer = Customer.objects.get(pk=instance.pk)
                    print('here!!!!', customer)
                    Cart.objects.create(customer=customer, product=product)
        return instance


class CustomerAdmin(UserAdmin):
    form = CustomerChangeForm

    def __init__(self, *args, **kwargs):
        super(CustomerAdmin, self).__init__(*args, **kwargs)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Cart'), {'fields': ('selected_products',)}),
        (('Personal info'), {'classes': ('collapse',)
                            ,'fields': ('first_name', 'last_name', 'email')}),
        (('Permissions'), {'classes': ('collapse',)
                          ,'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (('Important dates'), {'classes': ('collapse',)
                              ,'fields': ('last_login', 'date_joined')}),
    )


# Register your models here.
admin.site.register(Product)
try:
    admin.site.unregister(get_user_model())
finally:
    admin.site.register(get_user_model(), CustomerAdmin)
