from behave import when, given, then


@given('I am a new user')
def impl(context):
    pass


@when('I visit the home page')
def impl(context):
    context.browser.get(context.server_url)


@then('I will see the text "{text}"')
def impl(context, text):
    page_text = context.browser.find_element_by_tag_name('body').text
    print(text, page_text)
    assert text in page_text
