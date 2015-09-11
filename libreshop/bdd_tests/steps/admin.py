import os
import string
import random
from behave import when, given, then


ADMIN_USER = os.environ.get('ADMIN_USER') or 'admin'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'


@given(u'I am a staff member')
def step_impl(context):
    pass


@when(u'I visit the admin login page')
def step_impl(context):
    context.browser.get(context.server_url + '/admin')


@when(u'I log in to the site admin page')
def step_impl(context):
    inputbox = context.browser.find_element_by_id('id_username')
    inputbox.send_keys(ADMIN_USER)
    inputbox = context.browser.find_element_by_id('id_password')
    inputbox.send_keys(ADMIN_PASSWORD)
    button = context.browser.find_element_by_xpath("//input[@type='submit']")
    button.submit()
    context.test.assertIn('Site administration | Django site admin', context.browser.title)


@when(u'I add a user named "{text}"')
def step_impl(context, text):
    # Enter text into the Username field.
    inputbox = context.browser.find_element_by_id('id_username')
    inputbox.send_keys(text)

    # Enter a random password into the Password field.
    random_password = ''.join(random.choice(string.ascii_letters+string.digits) for i in range(8))
    inputbox = context.browser.find_element_by_id('id_password1')
    inputbox.send_keys(random_password)

    # Repeat the random password in the Password Confirmation field.
    inputbox = context.browser.find_element_by_id('id_password2')
    inputbox.send_keys(random_password)

    # Click the save button on the Add User page.
    submit_button = context.browser.find_element_by_xpath("//input[@class='default']")
    submit_button.click()

    # Click the save button on the Change User page.
    submit_button = context.browser.find_element_by_xpath("//input[@class='default']")
    submit_button.click()


@when(u'I add a product called "{text}"')
def step_impl(context, text):
    # Enter text into the Name field.
    inputbox = context.browser.find_element_by_id('id_name')
    inputbox.send_keys(text)

    # Click the save button on the Add Product page.
    submit_button = context.browser.find_element_by_xpath("//input[@class='default']")
    submit_button.click()
