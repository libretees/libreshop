from behave import when, given, then
from custom.django import DjangoStep


@given(u'I am a new user')
def step_impl(context):
    pass


@given(u'I am an authenticated user')
def step_impl(context):
    pass


@when(u'I visit the home page')
def step_impl(context):
    context.browser.get(context.server_url)
