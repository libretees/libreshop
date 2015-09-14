# Import Python module(s)
import logging

from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

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

    def form_invalid(self, form):
        return HttpResponse(form.errors)
