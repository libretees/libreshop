from behave import when, given, then

@when(u'I visit the user registration page')
def step_impl(context):
    context.browser.get(context.server_url + '/user/register')
