from django.conf.urls import url
from orders.views import CheckoutFormView, ConfirmationView


urlpatterns = [
    url(r'^$', CheckoutFormView.as_view(), name='main'),
    url(r'^complete/', ConfirmationView.as_view(), name='confirmation'),
]
