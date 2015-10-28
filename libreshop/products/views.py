import logging
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.base import TemplateView
from products.forms import ProductOrderForm
from products.models import Product

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your views here.
class HomepageView(TemplateView):

    template_name = 'products/featured.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        product = None
        try:
            product = Product.objects.get(sku='1000') or None
        except ObjectDoesNotExist as e:
            logger.info('Featured product does not exist.')

        if product:
            context['product'] = product
            context['form'] = ProductOrderForm(product)
        return context
