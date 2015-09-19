import hashlib
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import exceptions


from customers.forms import RegistrationToken

from .serializers import UserSerializer, GroupSerializer, RegistrationTokenSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    model = User


    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


    def get_permissions(self):

        permissions = None
        if self.request.method in ['GET', 'PUT', 'PATCH']:
            permissions = (IsAuthenticated(),)
        if self.request.method == 'POST':
        # allow non-authenticated user to create via POST
            permissions = (AllowAny(),)

        return permissions

    def update(self, request, *args, **kwargs):
        data = request.data

        password = data.get('password', None)
        if password:
            data['password'] = make_password(password)

        return super(UserViewSet, self).update(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        data = request.data

        self._validate_captcha(request, *args, **kwargs)

        with transaction.atomic():

            user = User.objects.create_user(
                username=data['username']
            )
            user.set_password(data['password'])
            user.save()

        serializer = UserSerializer(user, context={'request': request})
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


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
