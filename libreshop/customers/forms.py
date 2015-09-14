# Import Python module(s)
import string
import time
import random
import base64
import hashlib
import logging

from django import forms
from django.conf import settings
from django.core import serializers
from django.contrib import admin
#from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models.fields.related import ManyToManyRel

from captcha.image import ImageCaptcha

from .models import Customer
from shop.models import Product, Cart

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


class CustomerRegistrationForm(UserCreationForm):

    captcha_response = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)

        token = None
        if not settings.DEBUG:
            seed = random.Random(int(round(time.time() * 1000)))
            random.seed(seed)
            token = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(6))
        else:
            token = 'test'
            
        self.token = token
        hash_object = hashlib.sha256(self.token.encode())
        hex_dig = hash_object.hexdigest()

        captcha = ImageCaptcha()
        image = captcha.generate(self.token)
        encoding = base64.b64encode(image.getvalue()).decode()
        self.image = 'data:image/png;base64,%s' % encoding

        self.fields['registration_token'] = forms.CharField(initial=hex_dig, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super(CustomerRegistrationForm, self).clean()

        registration_token = cleaned_data.get("registration_token")
        captcha_response = cleaned_data.get("captcha_response")

        captcha_hash = hashlib.sha256(captcha_response.encode())
        captcha_hash = captcha_hash.hexdigest()
        print(registration_token, captcha_hash)

        if captcha_hash != registration_token:
            forms.ValidationError('Captcha is incorrect')

        return cleaned_data
