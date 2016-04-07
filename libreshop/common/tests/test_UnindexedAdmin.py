from django.contrib.admin import site
from django.db.models import Model
from django.http import HttpRequest
from django.test import TestCase
from ..admin import UnindexedAdmin
from ..models import Location

# Create your tests here.
class UnindexedAdminTest(TestCase):

    def test_admin_returns_empty_permissions_dict(self):
        '''
        Test that the UnindexedAdmin Mixin/ModelAdmin returns an empty
        permssions dict, that causes it to be hidden from the admin page index.
        '''
        request = HttpRequest()
        model_admin = UnindexedAdmin(model=Location, admin_site=site)
        permissions = model_admin.get_model_perms(request)
        self.assertEqual(permissions, {})
