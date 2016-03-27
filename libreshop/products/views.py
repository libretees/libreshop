import logging
from django.forms import Form
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from carts.utils import SessionCart
from .forms import ProductOrderForm
from .models import Product, Variant

logger = logging.getLogger(__name__)

# Create your views here.
class HomePageView(TemplateView):

    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        cart = SessionCart(self.request.session)

        context.update({
            'products': [
                product for product in Product.objects.all() if product.salable
            ],
            'cart': cart
        })

        return context



class ProductView(FormView):

    form_class = Form
    template_name = 'products/featured.html'
    success_url = '/'

    def __init__(self, *args, **kwargs):
        self.product = None
        super(ProductView, self).__init__(*args, **kwargs)


    def dispatch(self, request, *args, **kwargs):

        slug = kwargs.get('slug')

        try:
            self.product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            pass

        return (
            redirect('products:home') if not self.product else
            super(ProductView, self).dispatch(request, *args, **kwargs)
        )


    def get_form(self):
        return (
            ProductOrderForm(self.product, **self.get_form_kwargs())
            if self.product else super(ProductView, self).get_form()
        )


    def form_valid(self, form):
        logger.info('%s is valid' % type(form).__name__)

        cart = SessionCart(self.request.session)

        variants = Variant.objects.filter(product=self.product)
        for variant in variants:
            relevant_attributes = {
                key:variant.attributes[key]
                for key in variant.attributes
                if key in form.cleaned_data
            }
            if relevant_attributes == form.cleaned_data:
                logger.info('User selected "%s"' % variant)
                cart.add(variant)
                break

        return super(ProductView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)

        cart = SessionCart(self.request.session)

        context.update({
            'product': self.product,
            'cart': cart
        })

        return context
