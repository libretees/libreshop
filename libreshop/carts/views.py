from django.core.urlresolvers import reverse
from django.views.generic import View
from django.shortcuts import redirect
from .utils import SessionList

# Create your views here.
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
