import hashlib
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import exceptions


from customers.forms import RegistrationToken

from addresses.models import Address
from orders.models import Order, Purchase

from .serializers import (
    UserSerializer, GroupSerializer, RegistrationTokenSerializer,
    OrderSerializer)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


    def get_permissions(self):

        permissions = None
        if self.request.method in ['GET', 'PUT', 'PATCH', 'HEAD']:
            permissions = (IsAuthenticated(),)
        if self.request.method in ['POST', 'OPTIONS']:
        # allow non-authenticated users to create via POST
        # and allow API capabilities to be described via OPTIONS
            permissions = (AllowAny(),)

        return permissions


    def create(self, request, *args, **kwargs):
        data = request.data

        self._validate_captcha(request, *args, **kwargs)

        # Get an email address, if one was specified.
        user_email_address = data.get('email', None)

        with transaction.atomic():

            user = User.objects.create_user(
                username=data['username'],
                password=data['password'],
                email=user_email_address
            )
            user.save()

        if user_email_address:
            email = EmailMessage(
                subject='Welcome to LibreShop!',
                body='Test',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user_email_address],
                bcc=[],
                connection=None,
                attachments=None,
                headers=None,
                cc=None,
                reply_to=None
            )
            email.send()

        serializer = UserSerializer(user, context={'request': request})
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


    def _validate_captcha(self, request, *args, **kwargs):
        data = request.data

        token = data.get('token', None)
        if not token:
            error = {'token': ['A registration token is required.'], 'description': ['This field may not be blank.']}
            raise exceptions.ValidationError(error)

        captcha = data.get('captcha', None)
        if not captcha:
            error = {'captcha': ['A CAPTCHA response is required.'], 'description': ['This field may not be blank.']}
            raise exceptions.ValidationError(error)

        token_hash = hashlib.sha256(captcha.encode()).hexdigest()

        if token != token_hash:
            error = {'captcha': ['CAPTCHA is invalid'], 'description': ['The supplied CAPTCHA response is invalid.']}
            raise exceptions.ValidationError(error)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class RegistrationTokenView(APIView):
    """
    API endpoint to obtain a user registration token.
    """
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        registration_token = RegistrationToken()
        serializer = RegistrationTokenSerializer(registration_token)

        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = (IsAdminUser,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, token=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
