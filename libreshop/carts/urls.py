from django.conf.urls import include, url
from .views import RemoveItemView

urlpatterns = [
    url(r'^remove/$', RemoveItemView.as_view(), name='remove_item'),
]
