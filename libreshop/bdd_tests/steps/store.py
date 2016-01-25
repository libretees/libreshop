from behave import when, given, then
from selenium.webdriver.support.ui import Select

@when(u'I visit the "{page_name}" page')
def step_impl(context, page_name):
    context.browser.get(context.get_url(page_name))


@when(u'I click the x button next to "{text}"')
def step_impl(context, text):
    button = context.browser.find_element_by_xpath(
        "//p[contains(text(), '%s')]/following-sibling::button" % (text,)
    )
    button.click()
