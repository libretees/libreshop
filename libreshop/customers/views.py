# Import Python module(s)
import logging

from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login

from social.apps.django_app.utils import psa

from .forms import CustomerRegistrationForm
from .tools import get_access_token


# Initialize logger
logger = logging.getLogger(__name__)


# Create your views here.
class CustomerCreateView(CreateView):
    template_name = 'customers/register.html'
    form_class = CustomerRegistrationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form, **kwargs):
        response = super(CreateView, self).form_valid(form)

        # From: https://docs.djangoproject.com/en/1.8/topics/auth/default/#how-to-log-a-user-in
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(self.request, user)

                # Redirect to a success page.
            #else:
                # Return a 'disabled account' error message
                #...
        #else:
            # Return an 'invalid login' error message.
            #...

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, **kwargs):
        return HttpResponse(form.errors)


# When we send a third party access token to that view
# as a GET request with access_token parameter,
# python social auth communicate with
# the third party and request the user info to register or
# sign in the user. Magic. Yeah.
@psa('social:complete')
def register_by_access_token(request, backend):

    token = request.GET.get('access_token')
    # here comes the magic
    user = request.backend.do_auth(token)
    if user:
        login(request, user)
        # that function will return our own
        # OAuth2 token as JSON
        # Normally, we wouldn't necessarily return a new token, but you get the idea
        return get_access_token(user)
    else:
        # If there was an error... you decide what you do here
        return HttpResponse("error")
