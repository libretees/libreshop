from behave import when, given, then


@when(u'I visit the "{page_name}" page')
def step_impl(context, page_name):
    context.browser.get(context.get_url(page_name))
