from django.forms import ModelForm
from .models import Order

class PaymentForm(ModelForm):
    class Meta:
        model = Order
        fields = ['payment_card']
