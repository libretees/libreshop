# Import Python module(s)
import hashlib
import logging
from operator import itemgetter

from django import forms
from django import http
from django.core import serializers
from django.core.exceptions import ValidationError
from django.contrib import admin
#from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models.fields.related import ManyToManyRel

from .models import Customer
from shop.models import Product, Cart

from .widgets import CaptchaWidget

# Initialize logger
logger = logging.getLogger(__name__)

class CustomerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Customer

    selected_products = forms.ModelMultipleChoiceField(Product.objects.all(),
                                                       widget=admin.widgets.FilteredSelectMultiple('Products', False),
                                                       required=False)

    def __init__(self, *args, **kwargs):
        super(CustomerChangeForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.initial['selected_products'] = [customer_cart.product for customer_cart in Cart.objects.filter(customer__user=self.instance.pk)]
            relation = ManyToManyRel(field=Customer,
                                     to=Product,
                                     through=Cart)
            self.fields['selected_products'].widget = admin.widgets.RelatedFieldWidgetWrapper(self.fields['selected_products'].widget,
                                                                                              relation,
                                                                                              admin.site)

    def save(self, *args, **kwargs):
        instance = super(CustomerChangeForm, self).save(*args, **kwargs)

        if instance.pk:
            for selected_product in [customer_cart.product for customer_cart in Cart.objects.filter(customer__user=self.instance.pk)]:
                if selected_product not in self.cleaned_data['selected_products']:
                    # remove a product that has been unselected
                    customer = Customer.objects.get(pk=instance.pk)
                    Cart.objects.filter(customer__pk=customer.pk, product__pk=selected_product.pk)[0].delete()

            for product in self.cleaned_data['selected_products']:
                if product not in [customer_cart.product for customer_cart in Cart.objects.filter(customer__user=self.instance.pk)]:
                    # add newly-selected products
                    customer = Customer.objects.get(user=instance.pk)
                    saved_product = serializers.serialize('json', [product], fields=('name', 'attributes'))
                    Cart.objects.create(customer=customer, product=product, saved_product=saved_product)
        return instance


class CustomerAdmin(UserAdmin):
    form = CustomerChangeForm

    def __init__(self, *args, **kwargs):
        super(CustomerAdmin, self).__init__(*args, **kwargs)

        # Collapse all auth.User fields except for the Username and Password fields.
        UserAdmin.fieldsets = ([(name, field_options.update({'classes': ('collapse',)}) if name else field_options)
                              for (name, field_options)
                               in UserAdmin.fieldsets])

    fieldsets = UserAdmin.fieldsets + (
        (('Cart'), {'fields': ('selected_products',)}),
    )

class CaptchaField(forms.MultiValueField):
    widget = CaptchaWidget

    def __init__(self, *args, **kwargs):
        fields_ = (
            forms.CharField(),
            forms.CharField()
        )
        super(CaptchaField, self).__init__(fields_, *args, **kwargs)

    def compress(self, values):
        return ':'.join(values)

class CustomerRegistrationForm(UserCreationForm):

    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(CustomerRegistrationForm, self).clean()

        captcha_data = self.cleaned_data.get("captcha")
        captcha_hash, captcha_response = itemgetter(0, 1)(captcha_data.split(':'))
        response_hash = hashlib.sha256(captcha_response.encode()).hexdigest()

        if captcha_hash != response_hash:
            # See: https://docs.djangoproject.com/en/1.8/ref/forms/validation/#raising-validation-error
            self.add_error('captcha', ValidationError('Invalid value', code='invalid'))

        return cleaned_data

    def form_invalid(self, form):
        return http.HttpResponse(form.errors)
