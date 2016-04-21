from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from ..views import ConfirmationView

class ConfirmationViewTest(TestCase):

    def test_view_returns_200_status_if_no_order_token_is_in_session_variables(self):
        '''
        Test that the template used by ProductView marks the Product.description
        field value as HTML-safe output.
        '''
        factory = RequestFactory()
        request = factory.get(reverse('checkout:confirmation'))

        # Set `session` manually, since middleware is not supported.
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)

        # Set `user` manually, since middleware is not supported.
        request.user = AnonymousUser()

        view = ConfirmationView.as_view()
        response = view(request)
        response = response.render()
        rendered_html = response.content.decode()

        self.assertEqual(response.status_code, 200)
