from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import AllowAny

from customers.forms import RegistrationToken

from .serializers import UserSerializer, GroupSerializer, RegistrationTokenSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    model = User
    permission_classes = (AllowAny,)
    queryset = User.objects.all().order_by('-date_joined')

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)


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
