from django.test import TestCase
from ..models import Address


# Create your tests here.
class AddressModelTest(TestCase):

    def test_model_plural_name_is_addresses(self):
        '''
        Test that Address model has 'addresses' set as its plural name.
        '''
        address = Address()
        plural_name = address._meta.verbose_name_plural
        self.assertEqual(plural_name, 'addresses')


    def test_model_has_recipient_name_field(self):
        '''
        Test that Address.recipient_name is present.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        self.assertIsNotNone(recipient_name)


    def test_model_recipient_name_field_is_not_required(self):
        '''
        Test that Address.recipient_name is not required.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        nullable = getattr(recipient_name, 'null', None)
        self.assertTrue(nullable)


    def test_model_recipient_name_field_can_be_blank(self):
        '''
        Test that Address.recipient_name allows blank values in forms.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        blank = getattr(recipient_name, 'blank', None)
        self.assertTrue(blank)


    def test_model_recipient_name_field_has_max_length(self):
        '''
        Test that Address.recipient_name max length is 64.
        '''
        address = Address()
        recipient_name = None
        try:
            recipient_name = address._meta.get_field('recipient_name')
        except:
            pass
        max_length = getattr(recipient_name, 'max_length', None)
        self.assertEqual(max_length, 64)


    def test_model_has_street_address_field(self):
        '''
        Test that Address.street_address is present.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        self.assertIsNotNone(street_address)


    def test_model_street_address_field_is_required(self):
        '''
        Test that Address.street_address is required.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        nullable = getattr(street_address, 'null', None)
        self.assertFalse(nullable)


    def test_model_street_address_field_cannot_be_blank(self):
        '''
        Test that Address.street_address does not allow blank values in forms.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        blank = getattr(street_address, 'null', None)
        self.assertFalse(blank)


    def test_model_street_address_field_has_max_length(self):
        '''
        Test that Address.street_address max length is 1024.
        '''
        address = Address()
        street_address = None
        try:
            street_address = address._meta.get_field('street_address')
        except:
            pass
        max_length = getattr(street_address, 'max_length', None)
        self.assertEqual(max_length, 1024)


    def test_model_has_locality_field(self):
        '''
        Test that Address.locality is present.
        '''
        address = Address()
        locality = None
        try:
            locality = address._meta.get_field('locality')
        except:
            pass
        self.assertIsNotNone(locality)


    def test_model_locality_field_is_required(self):
        '''
        Test that Address.locality is required.
        '''
        address = Address()
        locality = None
        try:
            locality = address._meta.get_field('locality')
        except:
            pass
        nullable = getattr(locality, 'null', None)
        self.assertFalse(nullable)


    def test_model_locality_field_cannot_be_blank(self):
        '''
        Test that Address.locality does not allow blank values in forms.
        '''
        address = Address()
        locality = None
        try:
            locality = address._meta.get_field('locality')
        except:
            pass
        blank = getattr(locality, 'null', None)
        self.assertFalse(blank)


    def test_model_locality_field_has_max_length(self):
        '''
        Test that Address.locality max length is 16.
        '''
        address = Address()
        locality = None
        try:
            locality = address._meta.get_field('locality')
        except:
            pass
        max_length = getattr(locality, 'max_length', None)
        self.assertEqual(max_length, 16)


    def test_model_has_region_field(self):
        '''
        Test that Address.region is present.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        self.assertIsNotNone(region)


    def test_model_region_field_is_required(self):
        '''
        Test that Address.region is required.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        nullable = getattr(region, 'null', None)
        self.assertFalse(nullable)


    def test_model_region_field_cannot_be_blank(self):
        '''
        Test that Address.region does not allow blank values in forms.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        blank = getattr(region, 'null', None)
        self.assertFalse(blank)


    def test_model_region_field_has_max_length(self):
        '''
        Test that Address.region max length is 16.
        '''
        address = Address()
        region = None
        try:
            region = address._meta.get_field('region')
        except:
            pass
        max_length = getattr(region, 'max_length', None)
        self.assertEqual(max_length, 16)


    def test_model_has_postal_code_field(self):
        '''
        Test that Address.postal_code is present.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        self.assertIsNotNone(postal_code)


    def test_model_postal_code_field_is_not_required(self):
        '''
        Test that Address.postal_code is not required.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        nullable = getattr(postal_code, 'null', None)
        self.assertTrue(nullable)


    def test_model_postal_code_field_can_be_blank(self):
        '''
        Test that Address.postal_code allows blank values in forms.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        blank = getattr(postal_code, 'blank', None)
        self.assertTrue(blank)


    def test_model_postal_code_field_has_max_length(self):
        '''
        Test that Address.postal_code max length is 16.
        '''
        address = Address()
        postal_code = None
        try:
            postal_code = address._meta.get_field('postal_code')
        except:
            pass
        max_length = getattr(postal_code, 'max_length', None)
        self.assertEqual(max_length, 16)


    def test_model_has_country_field(self):
        '''
        Test that Address.country is present.
        '''
        address = Address()
        country = None
        try:
            country = address._meta.get_field('country')
        except:
            pass
        self.assertIsNotNone(country)


    def test_model_country_field_is_required(self):
        '''
        Test that Address.country is required.
        '''
        address = Address()
        country = None
        try:
            country = address._meta.get_field('country')
        except:
            pass
        nullable = getattr(country, 'null', None)
        self.assertFalse(nullable)


    def test_model_country_field_cannot_be_blank(self):
        '''
        Test that Address.country does not allow blank values in forms.
        '''
        address = Address()
        country = None
        try:
            country = address._meta.get_field('country')
        except:
            pass
        blank = getattr(country, 'null', None)
        self.assertFalse(blank)


    def test_model_renders_contents_as_html_markup(self):
        '''
        Test that the Address model renders its output as HTML markup.
        '''
        address = Address(
            recipient_name = 'Foo Bar',
            street_address = 'Apt 123\r\nTest St',
            locality = 'Test',
            region = 'OK',
            postal_code = '12345',
            country = 'US'
        )

        markup = (
            'Foo Bar<br />'
            'Apt 123<br />'
            'Test St<br />'
            'Test, OK  12345<br />'
            'United States of America'
        )

        render = address.render()

        self.assertEqual(render, markup)
