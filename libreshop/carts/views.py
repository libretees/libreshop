import logging
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.shortcuts import redirect
from products.models import Variant
from .utils import SessionCart, SessionList

# Initialize logger.
logger = logging.getLogger(__name__)

# Create your views here.
class AddItemView(View):

    def post(self, request):
        sku = request.POST.get('sku', None)

        if sku:
            enabled_variants = Variant.objects.filter(
                enabled=True, product__sku__istartswith=sku[0],
                sub_sku__iendswith=sku[-1]
            )
            variant = next(
                (_ for _ in enabled_variants if _.sku == sku),
                None
            )

            if variant:
                cart = SessionCart(request.session)
                cart.add(variant)
        else:
            logger.error('SKU not found!')

        next_url = request.POST.get('next', reverse('home'))

        return redirect(next_url, permanent=False)


class RemoveItemView(View):

    def post(self, request):

        index = request.POST.get('remove', None)

        if index:
            cart = SessionList(request.session)
            try:
                del cart[int(index)]
            except IndexError as e:
                pass

        next_url = request.POST.get('next', reverse('home'))

        return redirect(next_url, permanent=False)
