import logging
from django.test import TestCase
from ..views import HomepageView

# Initialize logger.
logger = logging.getLogger(__name__)

class HomepageViewTest(TestCase):
    def test_view_uses_featured_products_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'products/featured.html')
