from django.core.urlresolvers import reverse
from django.test import TestCase


class HomePageViewTest(TestCase):

    def setUp(self):
        '''
        Create common test assets prior to each individual unit test run.
        '''
        self.view_url = reverse('products:home')


    def test_view_returns_200_status(self):
        '''
        Test that the View returns a 200 OK status when it receives an HTTP GET
        request.
        '''
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)