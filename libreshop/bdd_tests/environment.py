import os
from django.conf import settings
from selenium import webdriver
try:
    from pyvirtualdisplay import Display
except ImportError:
    pass
import factories

HEADLESS_TEST = 'Display' in globals().keys()

os.environ['DJANGO_SETTINGS_MODULE'] = 'libreshop.settings'


def before_all(context):
    if HEADLESS_TEST:
        context.display = Display(visible=0, size=(1366, 768))
        context.display.start()

    context.browser = webdriver.Firefox()
    context.browser.set_window_size(1366, 768)

    # Wait a maximum of 3 seconds if an element is not present.
    context.browser.implicitly_wait(5)

    # Store Live Server URL.
    context.server_url = 'http://%s' % os.environ.get('DJANGO_LIVE_TEST_SERVER_ADDRESS', 'localhost:8081')


def after_all(context):
    # Take a screenshot before quitting.
    context.browser.save_screenshot('browser.png')

    # Close the browser.
    context.browser.quit()

    if HEADLESS_TEST:
        context.display.stop()


def before_feature(context, feature):
    pass


def after_feature(context, feature):
    pass


def before_scenario(context, scenario):
    if scenario.name in [
        'get a list of users as an admin',
        'get a list of users as a regular user',
        'get a list of users as an anonymous user',
    ]:
        # Create 3 users.
        users = [factories.UserFactory(username='user%s' % i) for i in range(3)]
    elif scenario.name in [
        'add a variant via the change user page' # steps/admin.py 
    ]:
        product = factories.ProductFactory()
        inventory = factories.InventoryFactory()
    elif scenario.name in [
        'add a product via the admin panel' # steps/admin.py
    ]:
        inventory = factories.InventoryFactory()


def after_scenario(context, scenario):
    pass


def before_step(context, step):
    """
    These run before every step.
    """
    if step.name in ['I am an admin',]:
        # Create an Admin account.
        admin = factories.AdminFactory()
    elif step.name in ['I am a staff member',]:
        # Create a Staff Member account.
        staff = factories.StaffMemberFactory()
    elif step.name in ['I am a regular user',]:
        # Create a User account.
        user = factories.UserFactory()
    elif step.name in ['I am an anonymous user',]:
        # Create a User account.
        user = factories.UserFactory()
    elif step.name in ['I visit the "home" page',]:
        # Create a product.
        product = factories.ProductFactory(
            option__Size=['Small', 'Medium', 'Large'],
            option__Color=['Black', 'White']
        )

def after_step(context, step):
    pass
