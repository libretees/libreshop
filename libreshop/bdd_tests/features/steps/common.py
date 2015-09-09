from behave import when, given, then


@then(u'I will see the text "{text}"')
def step_impl(context, text):
    page_text = context.browser.find_element_by_tag_name('body').text
    context.test.assertIn(text, page_text)


@then(u'I will see "{text}" in the browser title')
def step_impl(context, text):
    context.test.assertIn(text, context.browser.title)
