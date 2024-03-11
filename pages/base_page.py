from datetime import datetime
from locators.locators_desktop import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    """ Wrapper for selenium operations """

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 15)
        self.ignored_exceptions = (NoSuchElementException, StaleElementReferenceException, NoSuchFrameException)
        self.wait_with_conditions = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignored_exceptions)

    def wait_for_element_with_conditions(self, element):
        return self.wait_with_conditions.until(EC.presence_of_element_located(element))

    def wait_for_element_be_clickable(self, element):
        return self.wait_with_conditions.until(EC.element_to_be_clickable(element))

    def click_continue_button(self):
        self.wait_for_element_with_conditions(CONTINUE_BUTTON)
        continue_button = self.wait.until(EC.element_to_be_clickable(CONTINUE_BUTTON))
        continue_button.click()

    def get_signup_input(self):
        signup_input = self.wait_for_element_with_conditions(SIGN_UP_INPUT)
        signup_input.clear()
        return signup_input

    def type_email_to_input(self, email):
        signup_input = self.get_signup_input()
        signup_input.send_keys(email)
        screenshot_name = 'enter_email_%s.png' % datetime.now().strftime('%Y%m%d_%H%M%S')

    def get_current_url(self):
        return self.driver.current_url

    def wait_till_url_changes(self):
        initial_url = self.get_current_url()
        self.wait.until(EC.url_changes(initial_url))

    def switch_to_iframe(self, locator):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))

    def find_all_elements(self, locator):
        return self.driver.find_elements(*locator)
