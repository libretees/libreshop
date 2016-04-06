from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import (
    APITestCase, APIRequestFactory
)
from ..views import RegistrationTokenView

User = get_user_model()

# Create your tests here.
class RegistrationTokenViewTest(APITestCase):

    def setUp(self):
        '''
        Create basic user/admin accounts needed to test this ViewSet.
        '''
        self.user = User.objects.create_user(
            username='user', password=make_password('user')
        )
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com',
            password=make_password('admin')
        )
        self.view = RegistrationTokenView.as_view()


    def test_view_returns_200_status_code_for_unauthenticated_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/token/')

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_returns_token_field_within_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/token/')

        response = self.view(request)
        response.render()

        fields = response.data.keys()

        self.assertIn('token', fields)


    def test_view_returns_image_field_within_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/token/')

        response = self.view(request)
        response.render()

        fields = response.data.keys()

        self.assertIn('image', fields)


    def test_view_returns_audio_field_within_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/token/')

        response = self.view(request)
        response.render()

        fields = response.data.keys()

        self.assertIn('audio', fields)
