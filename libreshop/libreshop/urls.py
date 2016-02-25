"""libreshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from products.views import HomePageView
import api.urls
import carts.urls
import customers.urls

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^checkout/', include('orders.urls', namespace='checkout')),
    # Add URL for Privacy Policy.
    url(r'^policy/privacy-policy',
        TemplateView.as_view(
            template_name='libreshop/privacy_policy.html'
        ),
        name='privacy-policy'
    ),
    # Add URL for Website Terms and Conditions.
    url(r'^policy/terms-and-conditions',
        TemplateView.as_view(
            template_name='libreshop/terms_and_conditions.html'
        ),
        name='terms-and-conditions'
    ),
    # Add URL for Refund Policy.
    url(r'^policy/return-policy',
        TemplateView.as_view(
            template_name='libreshop/return_policy.html'
        ),
        name='return-policy'
    ),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^api/', include(api.urls)),
    url(r'^cart/', include(carts.urls)),
    url(r'^user/', include(customers.urls)),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
