import logging
import time
from config_parsers.config_analytics_systems_url_parser import ConfigAnalyticsSystemsUrlParser
from helpers.helpers import parse_network_request_data
from locators.locators_desktop import *
from pages.signup_page import SignUpPage
from selenium.webdriver.common.keys import Keys


class CheckoutPage(SignUpPage):
    STRIPE_URL = 'stripe'
    REQUEST_PATH = 'confirm'

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def go_to_checkout_page(self, domain_url, user_email):
        self.open_signup_page(domain_url)
        self.create_account(user_email)

    def get_subscription_item(self, button_name):
        sub_btn = self.wait_for_element_with_conditions(button_name)
        return sub_btn

    def wait_till_checkout_form_visible(self):
        self.wait_for_element_with_conditions(COME_BACK_BUTTON)

    def select_subscription_plan(self, subscription_plan):
        locator = self.get_subscription_item(PLAN_BUTTON_1)
        if subscription_plan == 2:
            locator = self.get_subscription_item(PLAN_BUTTON_2)
        elif subscription_plan == 3:
            locator = self.get_subscription_item(PLAN_BUTTON_3)
        locator.click()
        self.click_continue_button()
        logging.info(f"Subscription plan {subscription_plan} is selected")
        self.wait_till_checkout_form_visible()

    def fill_checkout_form_with_card_data(self, card_data):

        self.switch_to_iframe(self.wait_for_element_with_conditions(CARD_NUMBER_IFRAME))
        card_number_input = self.wait_for_element_with_conditions(CARD_NUMBER_ELEMENT)
        card_number_input.clear()
        card_number_input.send_keys(card_data['card_number'])
        self.driver.switch_to.default_content()

        self.switch_to_iframe(self.wait_for_element_with_conditions(CARD_EXPIRY_IFRAME))
        card_expiry_input = self.wait_for_element_with_conditions(CARD_EXPIRY_ELEMENT)
        card_expiry_input.clear()
        card_expiry_input.send_keys(card_data['expire_date'])
        self.driver.switch_to.default_content()

        self.switch_to_iframe(self.wait_for_element_with_conditions(CARD_CVV_IFRAME))
        card_cvv_input = self.wait_for_element_with_conditions(CARD_CVV_ELEMENT)
        card_cvv_input.clear()
        card_cvv_input.send_keys(card_data['cvv'])
        self.driver.switch_to.default_content()

        cardholder_name = self.wait_for_element_with_conditions(CARDHOLDER_NAME_ELEMENT)
        if cardholder_name:
            cardholder_name.clear()
            cardholder_name.send_keys(card_data['cardholder_name'])

        logging.info(f"Checkout form is filled with card {card_data['card_number']}")

    def get_payment_intent_request(self):
        config_parser = ConfigAnalyticsSystemsUrlParser()
        stripe_url = config_parser.get_request_url_by_key(self.STRIPE_URL)
        request_data = parse_network_request_data(self.driver, stripe_url, self.REQUEST_PATH, timeout=30)
        logging.info("Payment intent request is received")
        return request_data

    def buy_stripe_subscription_with_3ds_window(self):
        # checkout page has a lot of continue-button ids
        continue_buttons = self.find_all_elements(CONTINUE_BUTTON)
        for button in continue_buttons:
            if button.is_displayed():
                self.wait_for_element_be_clickable(button)
                button.click()
                break

        request_data = self.get_payment_intent_request()
        payment_intent_request = request_data[0]
        expected_status = 'requires_action'
        current_status = payment_intent_request['response_body']['status']
        assert current_status == expected_status, (f"Wrong status in api.stripe request. Should be '{expected_status}'"
                                                   f", '{current_status}' received")

        iframe_not_found = True
        # need to wait for stripe iframe to be loaded
        time.sleep(3)
        iframes = self.find_all_elements(IFRAME)
        for iframe in iframes:
            self.switch_to_iframe(iframe)
            iframe_3ds = self.find_all_elements(STRIPE_3DS_IFRAME)
            if iframe_3ds:
                iframe_not_found = False
                self.switch_to_iframe(iframe_3ds[0])
                logging.info(f"Switched to 3ds iframe")
                button = self.wait_for_element_be_clickable(STRIPE_3DS_CONFIRM_BUTTON)
                # firefox doesn't work with .click() here
                button.send_keys(Keys.RETURN)
                self.driver.switch_to.default_content()
                break
            else:
                self.driver.switch_to.default_content()

        if iframe_not_found:
            raise ModuleNotFoundError("3ds window for Stripe payment is not found")
        logging.info("3ds window is confirmed")
        self.wait_till_url_changes()

    def buy_subscription_without_3ds(self):
        # checkout page has a lot of continue-button ids
        continue_buttons = self.find_all_elements(CONTINUE_BUTTON)
        for button in continue_buttons:
            if button.is_displayed():
                self.wait_for_element_be_clickable(button)
                button.click()
                break

        logging.info("3ds window is not expected here and not shown")
        self.wait_till_url_changes()
