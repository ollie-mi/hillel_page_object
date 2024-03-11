import json
import logging


class ExpectedPagesConfigParser:
    """ Parses config with expected pages
    Config example:
        domain: {
            'current_page': 'next_page'
        }
    """

    def __init__(self, config_path):
        self.config_data = self._load_config_data(config_path)

    @staticmethod
    def _load_config_data(config_path) -> dict:
        """Load config data from the file."""
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
            return config_data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading config file from {config_path}: {e}")
            return {}

    def _get_config_by_domain(self, domain: str) -> dict:
        """Get config for specific domain"""
        return self.config_data.get(domain, {})

    def get_expected_next_page(self, domain: str, landing: str, current_page: str) -> str:
        """Get config for current page"""
        if len(landing) == 0:
            landing = 'default'
        domain_config = self._get_config_by_domain(domain)
        landing_config = domain_config.get(landing, {})

        if landing_config is None:
            raise ValueError(
                f"No expected pages configured for domain: {domain}, landing: {landing}")

        next_page = landing_config.get(current_page, '')
        if not next_page:
            raise ValueError(f"Wrong 'current_page' value: {current_page}. Config does not exists")
        logging.info(f"Expected next page is received: {next_page}")
        return next_page
