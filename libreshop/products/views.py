import logging
from django.views.generic import FormView
from carts import SessionList
from products.forms import ProductOrderForm
from products.models import Product, Variant

logger = logging.getLogger(__name__)

# Create your views here.
class HomePageView(FormView):

    template_name = 'products/featured.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(sku='1000')
        except Product.DoesNotExist:
            product = Product.objects.create(sku='1000', name='foo')

        return super(HomePageView, self).dispatch(request, *args, **kwargs)


    def get_form(self):
        try:
            product = Product.objects.get(sku='1000')
        except Product.DoesNotExist:
            product = Product.objects.create(sku='1000', name='foo')

        return ProductOrderForm(product, **self.get_form_kwargs())


    def form_valid(self, form):
        logger.info('%s is valid' % type(form).__name__)

        product = Product.objects.get(sku='1000')
        cart = SessionList(self.request.session)

        variants = Variant.objects.filter(product=product)
        for variant in variants:
            relevant_attributes = {
                key:variant.attributes[key]
                for key in variant.attributes
                if key in form.cleaned_data
            }
            if relevant_attributes == form.cleaned_data:
                logger.info('User selected "%s"' % variant)
                cart.append(variant.id)
                break

        return super(HomePageView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        product = Product.objects.get(sku='1000')

        session_cart = SessionList(self.request.session)
        cart = [
            variant for pk in session_cart
            for variant in Variant.objects.filter(pk=pk)
        ]
        total = sum(variant.price for variant in cart)

        context.update({
            'product': product,
            'cart': cart,
            'total': total,
        })

        return context
