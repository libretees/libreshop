import logging
from django.test import TestCase
from ..views import HomepageView

# Initialize logger.
logger = logging.getLogger(__name__)

class HomepageViewTest(TestCase):

    def test_view_uses_featured_products_template(self):
        '''
        Test that the view uses the products/featured.html template.
        '''
        response = self.client.get('')
        self.assertTemplateUsed(response, 'products/featured.html')


    def test_template_includes_csrf_token(self):
        '''
        Test that the view's template includes a CSRF token.
        '''
        response = self.client.get('')
        csrf_token_regex = "<input type='hidden' name='csrfmiddlewaretoken' value='[A-Za-z0-9]{32}' />"
        rendered_html = response.content.decode()
        self.assertRegex(rendered_html, csrf_token_regex)
