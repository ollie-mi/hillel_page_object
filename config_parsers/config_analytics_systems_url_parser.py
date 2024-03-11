import json
import logging
from globals import dir_globals


class ConfigAnalyticsSystemsUrlParser:
    """ Parses config with analytics systems urls"""
    ANALYTICS_SYSTEMS_URLS = 'analytics_systems_urls'
    REQUEST_URLS = 'request_urls'

    def __init__(self):
        self.config_data = self._load_config_data(dir_globals.ANALYTICS_SYSTEMS_URLS_CONFIG)

    @staticmethod
    def _load_config_data(config_path):
        """Get config data from the file"""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return config_data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading config file from {config_path}: {e}")
            return None

    def get_analytics_systems_urls_by_key(self, key: str, env: str) -> str:
        """Get specific event system by key"""
        if self.config_data is None:
            raise ValueError("Analytics Systems Config data is not loaded.")
        event_url_dict = self.config_data.get(self.ANALYTICS_SYSTEMS_URLS, {}).get(key.lower(), {})
        event_url = event_url_dict.get(env)
        if event_url_dict is None:
            raise ValueError(f"Analytics system with key '{key}' does not exist in the config.")
        logging.info("URLs for the specific analytic system is received.")
        return event_url

    def get_request_url_by_key(self, key: str) -> str:
        """Get specific request url by key"""
        if self.config_data is None:
            raise ValueError("Analytics Systems Config data is not loaded.")
        request_url = self.config_data.get(self.REQUEST_URLS, {}).get(key.lower())
        if request_url is None:
            raise ValueError(f"Request url with key '{key}' does not exist in the config.")
        logging.info("URL for the specific request is received.")
        return request_url

    def get_all_analytics_urls(self) -> set:
        """Get all analytics systems URLs. Returns list"""
        if self.config_data is None:
            raise ValueError("Config data is not loaded.")
        event_url_config = self.config_data.get(self.ANALYTICS_SYSTEMS_URLS, {})
        if not event_url_config:
            raise ValueError(f"Key {self.ANALYTICS_SYSTEMS_URLS} is empty or does not exist in the config.")
        event_urls_list = []
        for system in event_url_config.values():
            for url in system.values():
                event_urls_list.append(url)
        logging.info("List of analytics systems URLs is received.")
        return set(event_urls_list)

    def get_all_request_urls(self) -> set:
        """Get all request URLs. Returns list"""
        if self.config_data is None:
            raise ValueError("Config data is not loaded.")
        request_url_config = self.config_data.get(self.REQUEST_URLS, {})
        if not request_url_config:
            raise ValueError(f"Key {self.REQUEST_URLS} is empty or does not exist in the config.")
        request_urls_list = [value for value in request_url_config.values()]
        logging.info("List of request URLs is received.")
        return set(request_urls_list)

    def get_all_network_requests_urls(self) -> list:
        """Get all URLs from the config. Returns list"""
        if self.config_data is None:
            raise ValueError("Config data is not loaded.")
        event_url_list = list(self.get_all_analytics_urls())
        request_url_list = list(self.get_all_request_urls())
        logging.info("List of network request URLs is received.")
        return event_url_list + request_url_list
