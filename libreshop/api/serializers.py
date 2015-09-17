from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'id', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RegistrationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    image = serializers.CharField()
    audio = serializers.CharField()
