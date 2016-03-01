from django.conf.urls import include, url
from .views import AddItemView, RemoveItemView

urlpatterns = [
    url(r'^add/$', AddItemView.as_view(), name='add'),
    url(r'^remove/$', RemoveItemView.as_view(), name='remove')
]
