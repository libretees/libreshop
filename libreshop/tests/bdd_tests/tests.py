import os
from subprocess import call
from django.test import LiveServerTestCase

# Cloud9 Environment variables
IP = os.environ.get('IP')
PORT = os.environ.get('PORT')

# Determine the Django Live Test Server address.
if (IP and PORT) and not os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS'):
    os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '%s:%s' % (IP, PORT)

BDD_TEST_PATH = os.path.dirname(__file__)

class TestBDD(LiveServerTestCase):

    def test_bdd_functionality(self):
        call('cd %s && behave' % BDD_TEST_PATH, shell=True)
