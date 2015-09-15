# Import Python module(s)
import logging

from django import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login

from .forms import CustomerRegistrationForm

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
