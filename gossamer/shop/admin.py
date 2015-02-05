from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Product, Cart, Customer


class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False


class CustomerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Cart


class CustomerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cart
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Customer.objects.get(username=username)
        except Customer.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class CustomerAdmin(UserAdmin):
    form = CustomerChangeForm
    add_form = CustomerCreationForm

    inlines = (CustomerInline,)


# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
try:
    admin.site.unregister(get_user_model())
finally:
    admin.site.register(get_user_model(), CustomerAdmin)
