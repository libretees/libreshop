import unittest
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
try:
    from pyvirtualdisplay import Display
    HEADLESS_TEST = True
except ImportError:
    HEADLESS_TEST = False

ADMIN_USER = os.environ.get('ADMIN_USER') or ''
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or ''

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        if HEADLESS_TEST:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        if HEADLESS_TEST:
            self.display.stop()

    def test_can_access_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Gossamer', self.browser.title)


class AdminUserTest(unittest.TestCase):

    def setUp(self):
        if HEADLESS_TEST:
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        if HEADLESS_TEST:
            self.display.stop()

    def test_can_access_page(self):
        self.browser.get('http://localhost:8000/admin')
        self.assertIn('Log in | Django site admin', self.browser.title)

    def test_can_log_in(self):
        self.browser.get('http://localhost:8000/admin')
        self.assertIn('Log in | Django site admin', self.browser.title)

        inputbox = self.browser.find_element_by_id('id_username')
        inputbox.send_keys(ADMIN_USER)
        inputbox = self.browser.find_element_by_id('id_password')
        inputbox.send_keys(ADMIN_PASSWORD)
        button = self.browser.find_element_by_xpath("//input[@type='submit']")
        button.submit()
        self.assertIn('Site administration | Django site admin', self.browser.title)
        self.browser.save_screenshot('screenshot.png')


if __name__ == '__main__':
    unittest.main(warnings='ignore')
