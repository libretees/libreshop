import logging
from django.views.generic import FormView, TemplateView
from django.shortcuts import redirect
from carts import SessionList
from .forms import ProductOrderForm
from .models import Product, Variant

logger = logging.getLogger(__name__)

# Create your views here.
class HomePageView(TemplateView):

    template_name = 'products/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)

        session_cart = SessionList(self.request.session)
        cart = [
            variant for pk in session_cart
            for variant in Variant.objects.filter(pk=pk)
        ]
        total = sum(variant.price for variant in cart)

        context.update({
            'products': [
                product for product in Product.objects.all() if product.salable
            ],
            'cart': cart,
            'total': total,
        })

        return context



class ProductView(FormView):

    template_name = 'products/featured.html'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):

        slug = kwargs.get('slug')

        product = None
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            pass

        self.product = product

        return (
            redirect('products:home') if not product else
            super(ProductView, self).dispatch(request, *args, **kwargs)
        )


    def get_form(self):
        return ProductOrderForm(self.product, **self.get_form_kwargs())


    def form_valid(self, form):
        logger.info('%s is valid' % type(form).__name__)

        cart = SessionList(self.request.session)

        variants = Variant.objects.filter(product=self.product)
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

        return super(ProductView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)

        session_cart = SessionList(self.request.session)
        cart = [
            variant for pk in session_cart
            for variant in Variant.objects.filter(pk=pk)
        ]
        total = sum(variant.price for variant in cart)

        context.update({
            'product': self.product,
            'cart': cart,
            'total': total,
        })

        return context
