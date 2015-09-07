from behave import when, given, then
from custom.django import DjangoStep


@given('I am a new user')
def impl(context):
    pass


@given('I am an authenticated user')
def impl(context):
    pass


@when('I visit the home page')
def impl(context):
    context.browser.get(context.server_url)


@then('I will see the text "{text}"')
class impl(DjangoStep):
    def impl(self, context, text):
        page_text = context.browser.find_element_by_tag_name('body').text
        self.assertIn(text, page_text)
    __code__= impl.__code__
