# Import Python module(s)
import string
import time
import random
import base64
import hashlib
import logging

import django
from django import forms
from .models import Customer
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.forms import Field, HiddenInput, CharField
from django.conf import settings
from captcha.image import ImageCaptcha

# Initialize logger
logger = logging.getLogger(__name__)


class CustomerRegistrationForm(UserCreationForm):

    captcha_response = CharField()

    def __init__(self, *args, **kwargs):
        super(CustomerRegistrationForm, self).__init__(*args, **kwargs)
        seed = random.Random(int(round(time.time() * 1000)))
        random.seed(seed)
        self.token = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(6))
        hash_object = hashlib.sha256(self.token.encode())
        hex_dig = hash_object.hexdigest()

        captcha = ImageCaptcha()
        image = captcha.generate(self.token)
        encoding = base64.b64encode(image.getvalue()).decode()
        self.image = 'data:image/png;base64,%s' % encoding

        self.fields['registration_token'] = CharField(initial=hex_dig, widget=HiddenInput())

    def clean(self):
        cleaned_data = super(CustomerRegistrationForm, self).clean()

        registration_token = cleaned_data.get("registration_token")
        captcha_response = cleaned_data.get("captcha_response")

        captcha_hash = hashlib.sha256(captcha_response.encode())
        captcha_hash = captcha_hash.hexdigest()
        print(registration_token, captcha_hash)

        if captcha_hash != registration_token:
            forms.ValidationError('Captcha is incorrect')

        return cleaned_data

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
