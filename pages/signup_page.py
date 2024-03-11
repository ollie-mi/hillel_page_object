from config_parsers.config_analytics_systems_url_parser import ConfigAnalyticsSystemsUrlParser
from globals import dir_globals
from helpers.helpers import parse_network_request_data, parse_network_events_data
from pages.base_page import BasePage
from closer_configs.onboarding_events_parser import CloserOnboardingEventsConfigParser
from closer_configs.onboarding_landing_type_parser import CloserOnboardingLandingTypeConfigParser


class SignUpPage(BasePage):

    PORTAL_CDN = 'portal_cdn'
    SIGNUP_PATH = 'signup'
    PAYMENT_SETTINGS_PATH = 'payments-settings'

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def open_main_page(self):
        self.driver.get(self.base_url + "?utm_source=" + dir_globals.UTM_SOURCE)

    def open_signup_page(self, domain_url):
        self.open_main_page()
        self.driver.get(domain_url + 'signup')

    def create_account(self, email):
        self.type_email_to_input(email)
        self.click_continue_button()
        self.wait_till_url_changes()

    def get_signup_request_from_network(self):
        config_parser = ConfigAnalyticsSystemsUrlParser()
        signup_url = config_parser.get_request_url_by_key(self.PORTAL_CDN)
        request_data = parse_network_request_data(self.driver, signup_url, self.SIGNUP_PATH)
        return request_data

    def get_payment_settings_request_from_network(self):
        config_parser = ConfigAnalyticsSystemsUrlParser()
        signup_url = config_parser.get_request_url_by_key(self.PORTAL_CDN)
        request_data = parse_network_request_data(self.driver, signup_url, self.PAYMENT_SETTINGS_PATH)
        return request_data

    def get_signup_analytic_events_from_network(self, env: str, analytic_system: str):
        """Get requests from network traffic for given environment and analytic system"""
        config_parser = ConfigAnalyticsSystemsUrlParser()
        event_urls = config_parser.get_analytics_systems_urls_by_key(analytic_system, env)
        requests_data = parse_network_events_data(self.driver, event_urls)
        return requests_data

    @staticmethod
    def get_screen_events_from_config(domain: str, landing: str, screen: str, analytic_system: str) -> list:
        """Get list of events from config for specific domain, screen and analytic system"""
        config_parser = CloserOnboardingEventsConfigParser()
        return config_parser.get_screen_event_list(domain, landing, screen, analytic_system)

    def get_screen_events_from_network(self, env: str, domain: str, landing: str, screen: str, analytic_system: str) -> dict:
        """Get requests from network traffic for specific screen"""
        event_list_config = self.get_screen_events_from_config(domain, landing, screen, analytic_system)
        network_events = self.get_signup_analytic_events_from_network(env, analytic_system)
        result = {}
        for event in network_events:
            event_type = event.get('event_type')
            if event_type in event_list_config:
                result[event_type] = event
        return result

    @staticmethod
    def get_landing_type_from_config(domain: str, landing: str) -> dict:
        """Get dict of landing type and app name for specific onboarding"""
        config_parser = CloserOnboardingLandingTypeConfigParser()
        return config_parser.get_onboarding_landing_type(domain, landing)
