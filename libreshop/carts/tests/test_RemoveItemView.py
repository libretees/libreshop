from importlib import import_module
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.test import TestCase
from ..utils import SessionList
from ..views import RemoveItemView

# Create your tests here.
class RemoveItemViewTest(TestCase):

    def test_view_redirects_to_home_page_if_next_post_variable_is_not_set(self):
        '''
        Test that the view redirects to the Home Page, by default, as part of
        the Post/Redirect/Get (PRG) flow, when the 'next' POST variable not set.
        '''
        url = reverse('cart:remove')
        home_url = reverse('home')

        response = self.client.post(url, {})

        self.assertRedirects(response, home_url)


    def test_view_redirects_to_location_set_in_next_post_variable(self):
        '''
        Test that the view redirects to the location set in the 'next' POST
        variable, as part of the Post/Redirect/Get (PRG) flow.
        '''
        url = reverse('cart:remove')

        response = self.client.post(url, {'next': 'http://www.example.com'})

        self.assertRedirects(response, 'http://www.example.com')


    def test_view_removes_item_in_cart_set_in_remove_post_variable(self):
        '''
        Test that the view removes the item within the cart at the position
        contained in the 'remove' POST variable.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        url = reverse('cart:remove')
        session_list1 = SessionList(request.session, ['foo', 'bar'])
        request.POST['remove'] = '1'

        view = RemoveItemView()
        response = view.post(request)

        session_list2 = SessionList(request.session)
        self.assertEqual(session_list2, ['foo'])


    def test_view_does_not_affect_cart_when_remove_post_variable_is_invalid(self):
        '''
        Test that the view does not affect the cart if the position specified in
        the 'remove' POST variable is not valid.
        '''
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        url = reverse('cart:remove')
        session_list1 = SessionList(request.session, ['foo', 'bar'])
        request.POST['remove'] = '3'

        view = RemoveItemView()
        response = view.post(request)

        session_list2 = SessionList(request.session)
        self.assertEqual(session_list2, ['foo', 'bar'])
