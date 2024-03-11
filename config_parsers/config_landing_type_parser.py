import json
import logging


class OnboardingLandingTypeConfigParser:
    """ Parses config with landing types and app names for every page of onboarding
    """
    LANDING_TYPES = 'landing_types'
    APP_NAMES = 'app_names'

    def __init__(self, landing_type_list_path, onboarding_landing_types_path):
        self.landing_types_list = self._load_config_data(landing_type_list_path)
        self.onboarding_landing_types = self._load_config_data(onboarding_landing_types_path)

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

    def _get_landing_type_by_id(self, landing_type_id: str) -> str:
        """Get landing type name from landing types list config"""
        return self.landing_types_list.get(self.LANDING_TYPES, {}).get(landing_type_id, '')

    def _get_app_name_by_id(self, app_name_id: str) -> str:
        """Get app name from landing types list config"""
        return self.landing_types_list.get(self.APP_NAMES, {}).get(app_name_id, '')

    def get_onboarding_landing_type(self, domain: str, landing: str) -> dict:
        """Get expected landing type and app name for specific onboarding"""
        if len(landing) == 0:
            landing = 'default'
        domain_landing_type_config = self.onboarding_landing_types.get(domain, {})
        landing_config_data = domain_landing_type_config.get(landing, {})

        if landing_config_data is None:
            message = f"No landing types configured for domain: {domain}, landing: {landing}"
            logging.error(message)
            raise ValueError(message)

        result = {}
        for key, value in landing_config_data.items():
            expected_value = ''
            if 'landing' in key:
                expected_value = self._get_landing_type_by_id(str(value))
            if 'app' in key:
                expected_value = self._get_app_name_by_id(str(value))
            if not expected_value:
                raise ValueError(f"Landing type id or app name is '{value}' is not found in landing type list config")
            result[key] = expected_value
        logging.info("Landing types are received from config")
        return result
