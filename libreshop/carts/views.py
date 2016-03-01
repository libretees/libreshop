from django.core.urlresolvers import reverse
from django.views.generic import View
from django.shortcuts import redirect
from products.models import Variant
from .utils import SessionList

# Create your views here.
class AddItemView(View):

    def post(self, request):
        sku = request.POST.get('sku', None)

        if sku:
            try:
                enabled_variants = Variant.objects.filter(enabled=True)
                variant = next(
                    (_ for _ in enabled_variants if _.sku == sku),
                    None
                )
            except Variant.DoesNotExist as e:
                pass

            if variant:
                cart = SessionList(request.session)
                cart.append(variant.pk)

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
