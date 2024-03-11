import json
import logging
from globals import dir_globals


class ConfigPaymentCardsParser:
    """ Parses config with analytics systems urls"""
    VALID_CARDS = 'valid_cards'
    DECLINE_CARDS = 'decline_cards'

    def __init__(self):
        self.config_data = self._load_config_data(dir_globals.PAYMENT_CARDS_CONFIG)

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

    def _get_payment_gateway_config(self, payment_gateway: str) -> dict:
        """Get config for specific payment_gateway."""
        return self.config_data.get(payment_gateway)

    def get_valid_card_by_payment_gateway_and_type(self, payment_gateway: str, card_type: str) -> dict:
        """Get card data from config by payment gateway and card type"""
        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)

        if payment_gateway_config is None:
            message = f"Check 'payment_cards_config'! Payment gateway '{payment_gateway}' does not exist"
            logging.error(message)
            raise ValueError(message)

        valid_cards = payment_gateway_config.get(self.VALID_CARDS)

        if valid_cards is None:
            message = f"Check 'payment_cards_config'! Section '{self.VALID_CARDS}' does not exist"
            logging.error(message)
            raise ValueError(message)

        card_data = valid_cards.get(card_type)

        if card_data is None:
            message = f"Check 'payment_cards_config'! Card type '{card_type}' does not exist"
            logging.error(message)
            raise ValueError(message)

        return card_data
