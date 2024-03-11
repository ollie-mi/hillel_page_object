import pytest
from config_parsers.config_payment_cards_parser import ConfigPaymentCardsParser
from closer_configs.expected_pages_config_parser import CloserExpectedPagesConfigParser
from closer_configs.supported_3ds_settings_parser import Closer3dsSettings
from pages.checkout_page import CheckoutPage


@pytest.mark.closer
@pytest.mark.checkout
class TestCheckoutPage:
    PAYMENT_GATEWAY = 'payment_gateway'
    PAYMENT_ACCOUNT = 'payment_account'
    DEFAULT_PAYMENT_ACCOUNT = 'v1'
    CURRENT_SCREEN = 'paywall'
    NEXT_SCREEN = 'checkout_form'
    expected_pages = CloserExpectedPagesConfigParser()
    payment_cards = ConfigPaymentCardsParser()
    supported_3ds_settings_config = Closer3dsSettings()

    @pytest.mark.checkout_ui
    def test_payment_with_valid_card_3ds_required(self, driver, parse_addoption_payment_settings, user_email,
                                                  subscription_plan):
        """Test opens signup page, creates account and buys every plan with 3ds required card. 3ds window should be
        displayed and confirmed. Verifies that current url is correct."""
        card_type = '3ds_required'
        payment_gateway = parse_addoption_payment_settings.get(self.PAYMENT_GATEWAY)
        if len(payment_gateway) == 0:
            payment_gateway = 'stripe'

        checkout = CheckoutPage(driver, self._base_url)
        checkout.go_to_checkout_page(self._domain_url, user_email)
        checkout.select_subscription_plan(subscription_plan)

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.CURRENT_SCREEN)
        expected_url = self._domain_url + expected_page
        current_url = checkout.get_current_url()
        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"

        card_data = self.payment_cards.get_valid_card_by_payment_gateway_and_type(payment_gateway, card_type)

        checkout.fill_checkout_form_with_card_data(card_data)
        if payment_gateway == 'stripe':
            checkout.buy_stripe_subscription_with_3ds_window()

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.NEXT_SCREEN)
        expected_url = self._domain_url + expected_page
        current_url = checkout.get_current_url()
        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"

    @pytest.mark.checkout_ui
    def test_payment_with_valid_card_3ds_supported(self, driver, parse_addoption_payment_settings, user_email,
                                                   subscription_plan):
        """Test opens signup page, creates account and buys every plan with 3ds supported card. 3ds window should be
        displayed if 3ds is switched for the payment account or onboarding. Verifies that current url is correct."""
        card_type = '3ds_supported'
        payment_gateway = parse_addoption_payment_settings.get(self.PAYMENT_GATEWAY)
        payment_account = parse_addoption_payment_settings.get(self.PAYMENT_ACCOUNT)
        if len(payment_gateway) == 0:
            payment_gateway = 'stripe'
        if len(payment_account) == 0:
            payment_account = self.DEFAULT_PAYMENT_ACCOUNT

        checkout = CheckoutPage(driver, self._base_url)
        checkout.go_to_checkout_page(self._domain_url, user_email)
        checkout.select_subscription_plan(subscription_plan)

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.CURRENT_SCREEN)
        expected_url = self._domain_url + expected_page
        current_url = checkout.get_current_url()
        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"

        card_data = self.payment_cards.get_valid_card_by_payment_gateway_and_type(payment_gateway, card_type)

        checkout.fill_checkout_form_with_card_data(card_data)
        is_3ds_supported_on = (
            self.supported_3ds_settings_config.is_3ds_supported_card_switched_on(payment_gateway, payment_account,
                                                                                 self._domain, self._landing))
        if payment_gateway == 'stripe' and is_3ds_supported_on:
            checkout.buy_stripe_subscription_with_3ds_window()
        else:
            checkout.buy_subscription_without_3ds()

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.NEXT_SCREEN)
        expected_url = self._domain_url + expected_page
        current_url = checkout.get_current_url()
        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"

    @pytest.mark.checkout_ui
    def test_payment_with_valid_card_3ds_not_supported(self, driver, parse_addoption_payment_settings, user_email,
                                                       subscription_plan):
        """Test opens signup page, creates account and buys every plan with 3ds not supported card. 3ds window is not
        displayed. Verifies that current url is correct."""
        card_type = '3ds_not_supported'
        payment_gateway = parse_addoption_payment_settings.get(self.PAYMENT_GATEWAY)
        payment_account = parse_addoption_payment_settings.get(self.PAYMENT_ACCOUNT)
        if len(payment_gateway) == 0:
            payment_gateway = 'stripe'
        if len(payment_account) == 0:
            payment_account = self.DEFAULT_PAYMENT_ACCOUNT

        checkout = CheckoutPage(driver, self._base_url)
        checkout.go_to_checkout_page(self._domain_url, user_email)
        checkout.select_subscription_plan(subscription_plan)

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.CURRENT_SCREEN)
        expected_url = self._domain_url + expected_page
        current_url = checkout.get_current_url()
        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"

        card_data = self.payment_cards.get_valid_card_by_payment_gateway_and_type(payment_gateway, card_type)

        checkout.fill_checkout_form_with_card_data(card_data)
        checkout.buy_subscription_without_3ds()

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.NEXT_SCREEN)
        expected_url = self._domain_url + expected_page
        current_url = checkout.get_current_url()
        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"
