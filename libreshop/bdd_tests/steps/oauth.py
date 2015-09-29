from behave import when, given, then

@when(u'I click the "{text}" button to authorize the app')
def step_impl(context, text):

    # Click a button displaying "text".
    if text == 'Okay': # Facebook OAuth Opt-In
        button = context.browser.find_element_by_xpath("//*[@id='platformDialogForm']/div[2]/table/tbody/tr/td[2]/button[2]")

    button.click()


@step(u'I will navigate to the "{id_provider}" app settings page')
def step_impl(context, id_provider):

    id_provider = id_provider.lower()

    url = None
    if id_provider == 'facebook':
        url = 'https://www.facebook.com/settings?tab=applications'
    elif id_provider == 'github':
        url = 'https://github.com/settings/applications'

    if not url:
        assert False
    else:
        context.id_provider = id_provider
        context.browser.get(url)


@step(u'I will remove the "{app}" app')
def step_impl(context, app):
    """
    Removes `applcation` from an ID Provider (IdP) so that OAuth tests can be
    rerunnable. This function assumes that you have navigated to the IdP via the
    'I will navigate to the "{id_provider}" app settings page' step.
    """
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions
    from selenium.webdriver.common.by import By

    if context.id_provider == 'facebook':
        # Locate the applicaiton <div> and the `X` button.
        div = context.browser.find_element_by_xpath("(//div[contains(text(), '%s')]/ancestor::div[contains(@class, 'clearfix')])[last()-1]" % app)
        remove_button = context.browser.find_element_by_xpath("(//div[contains(text(), '%s')]//preceding::a[@aria-label='Remove'])[last()]/i" % app)

        # Hover over the application <div> element so that the `X` button displays, then click the `X` button.
        ActionChains(context.browser).move_to_element(div).click(remove_button).perform()

        # Wait up to 60 seconds for the modal dialog to display.
        wait = WebDriverWait(context.browser, 60)
        element = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//span[contains(text(), 'Remove %s')]" % app)))

        # Click the `Remove` button.
        confirmation_button = context.browser.find_element_by_xpath("//input[@value='Remove']")
        confirmation_button.click()

    elif context.id_provider == 'github':
        # Locate the `Revoke` link and click it.
        revoke_link = (("//a[contains(text(), '%s')]" +
                        "/parent::div" +
                        "/following-sibling::div" +
                        "/a[contains(text(),'Revoke')]") % app)
        revoke_link = context.browser.find_element_by_xpath(revoke_link)
        revoke_link.click()

        # Confirm that we wish to revoke access.
        wait = WebDriverWait(context.browser, 60)
        revoke_button = ("//h2[contains(text(), 'Are you sure you want to revoke authorization?')]" +
                         "/ancestor::div[@role='dialog']" +
                         "//button[contains(text(), 'I understand, revoke access')]")
        revoke_button = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, revoke_button)))
        revoke_button.click()
