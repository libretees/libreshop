import os
from selenium import webdriver
try:
    from pyvirtualdisplay import Display
except ImportError:
    pass

HEADLESS_TEST = 'Display' in globals().keys()


def before_all(context):
    if HEADLESS_TEST:
        context.display = Display(visible=0, size=(1366, 768))
        context.display.start()

    context.browser = webdriver.Firefox()
    
    # Wait a maximum of 3 seconds if an element is not present.
    context.browser.implicitly_wait(3)

    # Store Live Server URL.
    context.server_url = 'http://%s' % os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS']


def after_all(context):
    context.browser.save_screenshot('browser.png')
    context.browser.quit()

    if HEADLESS_TEST:
        context.display.stop()


def before_feature(context, feature):
    pass
