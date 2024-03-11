import json
import logging


class ConfigOnboardingUrlParser:
    """ Parses Closer Onboarding urls"""
    ENV = 'env'
    DOMAIN = 'domain'
    LANDING = 'landing'

    def __init__(self, config_file_path):
        self.config_data = self._load_config_data(config_file_path)

    @staticmethod
    def _load_config_data(config_path):
        """Load config data from file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading config file from {config_path}: {e}")
            return {}

    def get_environment_config(self, request_body: dict) -> dict:
        """Get onboarding config for specific environment"""
        env = request_body.get(self.ENV)
        if not env:
            raise ValueError(f"Key '{self.ENV}' is not found in request_body")

        env = env.lower()
        env_config = self.config_data.get('url', {}).get(env)
        if not env_config:
            raise ValueError(f"Wrong 'environment' value: {env}")

        logging.info("Environment config is received")
        return env_config

    def get_domain_name(self, request_body: dict) -> str:
        """Get domain name from request_body"""
        domain = request_body.get(self.DOMAIN)
        if not domain:
            raise ValueError(f"Key '{self.DOMAIN}' is not found in request_body")
        return domain

    def get_domain_url(self, request_body: dict) -> str:
        """Get domain url from config for specific domain"""
        env_data = self.get_environment_config(request_body)
        domain = self.get_domain_name(request_body)

        domain_url = env_data.get(domain)
        if domain_url is None:
            raise ValueError(f"Domain '{domain} is not found in Onboarding Urls Config")
        elif not domain_url:
            raise ValueError("Domain url is not found in Onboarding Urls Config")

        if not domain_url.endswith('/'):
            domain_url += '/'

        logging.info("Domain url is received")
        return domain_url

    def get_landing_config(self) -> dict:
        """Get landings config"""
        landing_config = self.config_data.get(self.LANDING)
        if landing_config is None:
            raise ValueError(f"fKey '{self.LANDING}' is not found in config")
        return landing_config

    def get_domain_landing_list(self, request_body: dict) -> list:
        """Get landing list from config for specific domain"""
        domain = request_body.get(self.DOMAIN)
        if not domain:
            raise ValueError(f"Key '{self.DOMAIN}' is not found in request_body")

        landings_data = self.get_landing_config()
        domain_landing_list = landings_data.get(domain)
        if domain_landing_list is None:
            raise ValueError(f"Key '{self.LANDING}' is not found in config")

        logging.info("Landing list is received")
        return domain_landing_list

    def get_onboarding_url(self, request_body: dict) -> str:
        """Get full onboarding url from config"""
        landing = request_body.get(self.LANDING, None)
        if landing is None:
            raise ValueError(f"Key '{self.LANDING}' is not found in request_body")

        domain_url = self.get_domain_url(request_body)
        domain_data_landings = self.get_domain_landing_list(request_body)

        onboarding_url = domain_url
        if landing in domain_data_landings:
            onboarding_url += landing
        elif landing:
            raise ValueError(f"Landing '{landing}' is not found in config for domain '{request_body.get(self.DOMAIN)}'")

        logging.info("Onboarding url is received")
        return onboarding_url
