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
    elif id_provider == 'twitter':
        url = 'https://twitter.com/settings/applications'
    elif id_provider == 'reddit':
        url = 'https://www.reddit.com/prefs/apps/'

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
    from selenium.webdriver.support.expected_conditions import element_to_be_clickable
    from selenium.webdriver.common.by import By

    if context.id_provider == 'facebook':
        # Locate the applicaiton <div> and the `X` button.
        xpath = (("(//div[contains(text(), '%s')]" +
                  "/ancestor::div[contains(@class, 'clearfix')])[last()-1]") % app)
        div = context.browser.find_element_by_xpath(xpath)
        xpath = (("(//div[contains(text(), '%s')]" +
                  "//preceding::a[@aria-label='Remove'])[last()]/i") % app)
        remove_button = context.browser.find_element_by_xpath(xpath)

        # Hover over the application <div> element so that the `X` button displays, then click the `X` button.
        ActionChains(context.browser).move_to_element(div).click(remove_button).perform()

        # Click the `Remove` button in the modal dialog.
        wait = WebDriverWait(context.browser, 60)
        xpath = "//input[@value='Remove']"
        confirmation_button = wait.until(element_to_be_clickable((By.XPATH, xpath)))
        confirmation_button.click()

    elif context.id_provider == 'github':
        # Locate the `Revoke` link and click it.
        xpath = (("//a[contains(text(), '%s')]" +
                  "/parent::div" +
                  "/following-sibling::div" +
                  "/a[contains(text(),'Revoke')]") % app)
        revoke_link = context.browser.find_element_by_xpath(xpath)
        revoke_link.click()

        # Confirm that we wish to revoke access.
        wait = WebDriverWait(context.browser, 60)
        xpath = ("//h2[contains(text(), 'Are you sure you want to revoke authorization?')]" +
                 "/ancestor::div[@role='dialog']" +
                 "//button[contains(text(), 'I understand, revoke access')]")
        revoke_button = wait.until(element_to_be_clickable((By.XPATH, xpath)))
        revoke_button.click()

    elif context.id_provider == 'twitter':
        # Locate the `Revoke access` button and click it.
        xpath = (("//strong[contains(text(), '%s')]" +
                  "//ancestor::div[@class='app']" +
                  "/button") % app)
        revoke_button = context.browser.find_element_by_xpath(xpath)
        revoke_button.click()

    elif context.id_provider == 'reddit':
        # Locate the `revoke access` link and click it.
        xpath = (("//h2[contains(text(), '%s')]" +
                  "//ancestor::div[@class='app-details']" +
                  "//parent::div" +
                  "//a[text()='revoke access']") % app)
        revoke_link = context.browser.find_element_by_xpath(xpath)
        revoke_link.click()

        # Confirm that we wish to revoke access.
        xpath = (("//h2[contains(text(), '%s')]" +
                  "//ancestor::div[@class='app-details']" +
                  "//parent::div" +
                  "//a[text()='yes']") % app)
        confirmation_link = context.browser.find_element_by_xpath(xpath)
        confirmation_link.click()
