import json
import logging


class Config3dsSettingsParser:
    """ Parses config with 3ds settings for supported card"""
    SUPPORTED_3DS_SETTINGS = '3ds_on_supported_card'

    def __init__(self, config_path):
        self.config_data = self._load_config_data(config_path)

    @staticmethod
    def _load_config_data(config_path) -> dict:
        """Load config data from the file."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading config file from {config_path}: {e}")
            return {}

    def _get_3ds_supported_card_settings_config(self) -> dict:
        """Get config for 3ds supported cards"""
        return self.config_data.get(self.SUPPORTED_3DS_SETTINGS, {})

    def _get_payment_gateway_config(self, payment_gateway: str) -> dict:
        """Get config for specific payment_gateway."""
        supported_3ds_config = self._get_3ds_supported_card_settings_config()
        return supported_3ds_config.get(payment_gateway, {})

    def _get_payment_account_config(self, payment_gateway: str, payment_account: str) -> dict:
        """Get config for specific payment_gateway and payment_account."""
        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)
        return payment_gateway_config.get(payment_account, {})

    def is_3ds_supported_card_switched_on(self, payment_gateway: str, payment_account: str, domain: str, landing: str):
        """Function verifies if 3ds is switched on for supported card for specific onboarding"""
        if len(landing) == 0:
            landing = 'default'

        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)
        payment_account_config = self._get_payment_account_config(payment_gateway, payment_account)

        if payment_gateway and len(payment_gateway_config) == 0:
            message = f"Check '3ds_settings_config.json'! Seems payment_gateway '{payment_gateway}' does not exists"
            logging.error(message)
            raise ValueError(message)

        if payment_account and len(payment_account_config) == 0:
            message = (f"Check '3ds_settings_config.json'! Seems payment_account '{payment_account}' does not exists "
                       f"in payment_gateway '{payment_gateway}'")
            logging.error(message)
            raise ValueError(message)

        onboarding_config = payment_account_config.get(domain)

        if onboarding_config is None:
            message = f"Check '3ds_settings_config.json'! Seems domain '{domain}' does not exists"
            logging.error(message)
            raise ValueError(message)

        return landing in onboarding_config
