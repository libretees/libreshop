import os
from behave import when, given, then
from custom.django import DjangoStep


ADMIN_USER = os.environ.get('ADMIN_USER') or 'admin'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'


@given(u'I am a staff member')
def step_impl(context):
    pass


@when(u'I visit the admin login page')
def step_impl(context):
    context.browser.get(context.server_url + '/admin')


@when(u'I log in from the admin login page')
def step_impl(context):
    context.browser.get(context.server_url + '/admin')
    inputbox = context.browser.find_element_by_id('id_username')
    inputbox.send_keys(ADMIN_USER)
    inputbox = context.browser.find_element_by_id('id_password')
    inputbox.send_keys(ADMIN_PASSWORD)
    button = context.browser.find_element_by_xpath("//input[@type='submit']")
    button.submit()
    context.browser.save_screenshot('login_page.png')
    context.test.assertIn('Site administration | Django site admin', context.browser.title)
    context.browser.save_screenshot('admin_page.png')
