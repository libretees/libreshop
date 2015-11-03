import logging
from django.views.generic import FormView, TemplateView
from carts import SessionList
from products.forms import ProductOrderForm
from products.models import Product, Variant

logger = logging.getLogger(__name__)

# Create your views here.
class HomepageView(FormView):

    template_name = 'products/featured.html'
    success_url = '/'

    def get_form(self):
        product = Product.objects.get(sku='1000')
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

        return super(HomepageView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)

        cart = list()
        session_cart = SessionList(self.request.session)
        for id in session_cart:
            try:
                variant = Variant.objects.get(id=id)
                cart.append(variant)
            except:
                pass

        context.update({
            'cart': cart
        })

        return context


class CheckoutView(TemplateView):

    template_name = 'libreshop/base.html'
