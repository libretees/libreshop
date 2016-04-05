#from django.core.urlresolvers import reverse
import hashlib
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import (
    APITestCase, APIRequestFactory, force_authenticate
)
from ..views import UserViewSet

User = get_user_model()

# Create your tests here.
class UserViewSetTest(APITestCase):

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
        self.view = UserViewSet.as_view(actions={
            'get': 'list',
            'post': 'create',
            'options': 'options'
        })


    def test_view_returns_403_status_code_for_unauthenticated_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/users/')

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_view_returns_200_status_code_for_authenticated_user_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_returns_200_status_code_for_authenticated_admin_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_returns_list_containing_user_for_user_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        users = User.objects.all()
        results = [result['username'] for result in response.data['results']]

        self.assertEqual(results, ['user'])


    def test_view_returns_list_of_all_users_for_admin_get_request(self):

        factory = APIRequestFactory()
        request = factory.get('/api/users/')
        force_authenticate(request, user=self.admin)

        response = self.view(request)
        response.render()

        users = User.objects.all()
        results = [result['username'] for result in response.data['results']]

        result = all(user.username in results for user in users)

        self.assertTrue(result)


    def test_view_returns_201_status_code_for_successful_user_creation(self):

        factory = APIRequestFactory()
        request = factory.post('/api/users/', {
            'username': 'new_user',
            'password': 'new_user',
            'token': hashlib.sha256('1234'.encode()).hexdigest(),
            'captcha': '1234'
        })

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_view_sends_email_for_successful_user_creation_when_email_field_is_supplied(self):

        factory = APIRequestFactory()
        request = factory.post('/api/users/', {
            'username': 'new_user',
            'password': 'new_user',
            'email': 'test@example.com',
            'token': hashlib.sha256('1234'.encode()).hexdigest(),
            'captcha': '1234'
        })

        response = self.view(request)
        response.render()

        self.assertEqual(len(mail.outbox), 1)


    def test_view_returns_400_status_code_when_incorrect_captcha_is_supplied(self):

        factory = APIRequestFactory()
        request = factory.post('/api/users/', {
            'username': 'new_user',
            'password': 'new_user',
            'token': hashlib.sha256('1234'.encode()).hexdigest(),
            'captcha': '4321'
        })

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_view_returns_400_status_code_when_token_field_is_not_supplied(self):

        factory = APIRequestFactory()
        request = factory.post('/api/users/', {
            'username': 'new_user',
            'password': 'new_user',
            'captcha': '1234'
        })

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_view_returns_400_status_code_when_captcha_field_is_not_supplied(self):

        factory = APIRequestFactory()
        request = factory.post('/api/users/', {
            'username': 'new_user',
            'password': 'new_user',
            'token': hashlib.sha256('1234'.encode()).hexdigest()
        })

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_view_returns_200_status_code_for_options_request(self):

        factory = APIRequestFactory()
        request = factory.options('/api/users')

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_response_for_options_request_describes_api_capabilities(self):

        factory = APIRequestFactory()
        request = factory.options('/api/users')

        response = self.view(request)
        response.render()

        self.assertIn('actions', response.data)


    def test_view_returns_403_status_code_for_unauthenticated_head_request(self):

        factory = APIRequestFactory()
        request = factory.head('/api/users/')

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_view_returns_200_status_code_for_authenticated_user_head_request(self):

        factory = APIRequestFactory()
        request = factory.head('/api/users/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_returns_200_status_code_for_authenticated_admin_head_request(self):

        factory = APIRequestFactory()
        request = factory.head('/api/users/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_view_returns_list_containing_user_for_user_head_request(self):

        factory = APIRequestFactory()
        request = factory.head('/api/users/')
        force_authenticate(request, user=self.user)

        response = self.view(request)
        response.render()

        users = User.objects.all()
        results = [result['username'] for result in response.data['results']]

        self.assertEqual(results, ['user'])


    def test_view_returns_list_of_all_users_for_admin_head_request(self):

        factory = APIRequestFactory()
        request = factory.head('/api/users/')
        force_authenticate(request, user=self.admin)

        response = self.view(request)
        response.render()

        users = User.objects.all()
        results = [result['username'] for result in response.data['results']]

        result = all(user.username in results for user in users)

        self.assertTrue(result)
