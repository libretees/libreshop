from django.contrib.auth.hashers import check_password
from rest_framework.test import APITestCase
from ..serializers import UserSerializer

# Create your tests here.
class UserSerializerTest(APITestCase):

    def test_serializer_rejects_undeclared_non_native_fields(self):
        data = {
            'username': 'foo',
            'password': 'bar',
            'foo': 'bar'
        }
        serializer = UserSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertFalse(is_valid)


    def test_serializer_accepts_token_non_native_field(self):
        data = {
            'username': 'foo',
            'password': 'bar',
            'token': 1234
        }
        serializer = UserSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertTrue(is_valid)


    def test_serializer_accepts_captcha_non_native_field(self):
        data = {
            'username': 'foo',
            'password': 'bar',
            'captcha': 1234
        }
        serializer = UserSerializer(data=data)
        is_valid = serializer.is_valid()

        self.assertTrue(is_valid)


    def test_serializer_hashes_password_field(self):
        data = {
            'username': 'foo',
            'password': 'bar'
        }
        serializer = UserSerializer(data=data)
        is_valid = serializer.is_valid()

        encoded_password = serializer.validated_data.get('password')
        result = check_password('bar', encoded_password)

        self.assertTrue(result)
