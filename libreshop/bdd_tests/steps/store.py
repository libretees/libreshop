from behave import when, given, then
from selenium.webdriver.support.ui import Select

@when(u'I visit the "{page_name}" page')
def step_impl(context, page_name):
    context.browser.get(context.get_url(page_name))

@when(u'I select "{option}" from the "{select}" field')
def step_impl(context, option, select):
    select = Select(
        context.browser.find_element_by_css_selector('#id_%s' % select)
    )
    select.select_by_visible_text(option)
