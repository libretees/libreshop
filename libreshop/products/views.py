from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from products.forms import ProductOrderForm
from products.models import Product

# Create your views here.
class HomepageView(TemplateView):

    template_name = 'products/featured.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        product = Product.objects.get(sku='1000')
        context['product'] = product
        context['form'] = ProductOrderForm(product)
        return context
