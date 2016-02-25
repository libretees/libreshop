from django.conf.urls import url
from .views import HomePageView, ProductView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^(?P<sku>.+)$', ProductView.as_view(), name='product'),
]
