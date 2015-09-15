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


@when(u'I click the plus icon next to the "{field}" field')
def step_impl(context, field):

    field = field.replace(' ', '_').lower()
    link = context.browser.find_element_by_id('add_id_%s' % field)
    link.click()


@then(u'I will see "{text}" in the "{field}" select box')
def step_impl(context, text, field):

    field = field.replace(' ', '_').lower()
    options = context.browser.find_elements_by_xpath("//select[@name='%s']/option" % field)

    selected_products = [option.text for option in options]

    context.test.assertIn(text, selected_products)


@when(u'I click the "{link}" link next to "{name}"')
def step_impl(context, link, name):

    link = context.browser.find_element_by_xpath("//th[a='%s']/following-sibling::td[a='%s']/a" % (name, link))
    link.click()
