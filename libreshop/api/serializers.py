import hashlib
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework import exceptions

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password',)
        non_native_fields = ('token', 'captcha',)
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)

    def to_internal_value(self, data):
        native_fields = self.Meta.fields
        non_native_fields = self.Meta.non_native_fields
        extra_fields = [field for field in data if field not in native_fields + non_native_fields]

        for field in extra_fields:
            error = {'%s' % field: ['Field is not recognized.'], 'description': ['The `%s` field is not permitted.' % field]}
            raise exceptions.ValidationError(error)

        native_data = {key:value for (key, value) in data.items() if key in native_fields}
        super(UserSerializer, self).to_internal_value(native_data)

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

        return data

    def create(self, validated_data):

        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class RegistrationTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    image = serializers.CharField()
    audio = serializers.CharField()
