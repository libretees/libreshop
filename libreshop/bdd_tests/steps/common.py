import os
from behave import when, given, then
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select


@given(u'I am an admin')
def step_impl(context):
    context.username = 'admin'
    context.password = 'admin'


@given(u'I am a staff member')
def step_impl(context):
    context.username = 'staff'
    context.password = 'staff'


@given(u'I am a regular user')
def step_impl(context):
    context.username = 'user'
    context.password = 'user'


@given(u'I am an anonymous user')
def step_impl(context):
    context.username = None
    context.password = None


@then(u'I will see the text "{text}"')
def step_impl(context, text):

    page_text = context.browser.find_element_by_tag_name('body').text
    context.test.assertIn(text, page_text)


@then(u'I will not see the text "{text}"')
def step_impl(context, text):

    page_text = context.browser.find_element_by_tag_name('body').text
    context.test.assertNotIn(text, page_text)


@then(u'I will see "{text}" in the browser title')
def step_impl(context, text):
    """
    Wait up to 10 seconds for the title specified by `text` to display in the
    browser title bar. This allows time to pass for page loads as well as for
    redirect chains.
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions

    wait = WebDriverWait(context.browser, 10)
    element = wait.until(expected_conditions.title_is(text))

    context.test.assertIn(text, context.browser.title)


@when(u'I click the "{text}" link')
def step_impl(context, text):

    link = context.browser.find_element_by_link_text(text)
    link.click()


@then(u'I will see a link for "{text}"')
def step_impl(context, text):

    link = context.browser.find_elements_by_link_text(text)
    assert link


@then(u'I will see a link labeled "{text}"')
def step_impl(context, text):

    link = context.browser.find_elements_by_link_text(text)

    if not link:
        # Try to find the link by XPath, since there may be hidden elements within the <a> tag's text.
        link = context.browser.find_element_by_xpath("//a[contains(text(), '%s')]" % text)

    assert link


@when(u'I switch to the popup window')
def step_impl(context):

    windows = context.browser.window_handles
    current_window = context.browser.current_window_handle
    popup_window = next(window for window in windows if window != current_window)

    context.browser.switch_to.window(popup_window)


@when(u'I switch to the main window')
def step_impl(context):

    windows = context.browser.window_handles
    main_window = next(window for window in windows)
    context.browser.switch_to.window(main_window)


@when(u'I click the "{text}" button')
def step_impl(context, text):

    # Click a button displaying "text".
    button = context.browser.find_element_by_xpath("//input[@value='%s']|//button[contains(text(), '%s')]" % (text, text))
    button.click()


@when(u'I enter "{text}" in the "{label}" field')
def step_impl(context, text, label):

    xpath = "//input[@id=(//label[text()='%s:']/@for)]" % label
    input_boxes = context.browser.find_elements_by_xpath(xpath)

    if not input_boxes:
        xpath = "//input[@id=(//label[contains(text(), '%s')]/@for)]" % label
        input_boxes = context.browser.find_elements_by_xpath(xpath)

    text = get_account_credentials(text)

    for input_box in input_boxes:
        input_box.send_keys(text)


def get_account_credentials(text):

    credentials = text

    if text == 'My Facebook Username':
        credentials = os.environ.get('FACEBOOK_USERNAME', None)
    elif text == 'My Facebook Password':
        credentials = os.environ.get('FACEBOOK_PASSWORD', None)
    elif text == 'My GitHub Username':
        credentials = os.environ.get('GITHUB_USERNAME', None)
    elif text == 'My GitHub Password':
        credentials = os.environ.get('GITHUB_PASSWORD', None)
    elif text == 'My Twitter Username':
        credentials = os.environ.get('TWITTER_USERNAME', None)
    elif text == 'My Twitter Password':
        credentials = os.environ.get('TWITTER_PASSWORD', None)
    elif text == 'My Reddit Username':
        credentials = os.environ.get('REDDIT_USERNAME', None)
    elif text == 'My Reddit Password':
        credentials = os.environ.get('REDDIT_PASSWORD', None)

    return credentials


@step(u'I take a screenshot named "{text}"')
def step_impl(context, text):

    context.browser.save_screenshot('%s.png' % text)


@then(u'I will see a "{text}" icon')
def step_impl(context, text):

    class_name = 'fa-%s' % text.replace(' ', '-').lower()
    icon = context.browser.find_element_by_class_name(class_name)

    context.test.assertIsNotNone(icon)


@when(u'I select "{option}" from the "{select}" field')
def step_impl(context, option, select):

    try:
        # Try to find the select element using the `id` attribute.
        select_element = context.browser.find_element_by_id('id_%s' % select)
    except NoSuchElementException as e:
        # Try to find the select element within an InlineModelAdmin.
        select_element = context.browser.find_element_by_xpath(
            "//td[@class='field-%s']//select" % select
        )

    select = Select(select_element)

    select.select_by_visible_text(option)
