import json
import logging


class ConfigEmailAliasParser:
    """ Parses config with email alias"""
    V1 = 'v1'
    DISCOUNT = 'discount'
    DISCOUNT_ALIAS = 'test.discount'
    PAYMENT_GATEWAY = 'payment_gateway'
    PAYMENT_ACCOUNT = 'payment_account'
    EMAIL_ALIAS = 'email_alias'
    ACCOUNT_NAME = 'account_name'

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

    def _get_payment_gateway_config(self, payment_gateway: str) -> dict:
        """Get config for specific payment_gateway."""
        return self.config_data.get(payment_gateway, {})

    def get_payment_account_alias(self, payment_gateway: str, payment_account: str) -> str:
        """Get alias for specific payment_gateway and payment_account."""
        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)
        email_aliases = payment_gateway_config.get(self.EMAIL_ALIAS, {})
        return email_aliases.get(payment_account, '')

    def get_discount_alias(self, payment_gateway: str) -> str:
        """Get alias for testing discounts."""
        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)
        email_aliases = payment_gateway_config.get(self.EMAIL_ALIAS, {})
        return email_aliases.get(self.DISCOUNT, self.DISCOUNT_ALIAS)

    def get_account_name_config(self, payment_gateway: str) -> dict:
        """Get account name config for payment gateway"""
        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)
        return payment_gateway_config.get(self.ACCOUNT_NAME, {})

    def get_email_alias_by_payment_gateway(self, payment_settings: dict) -> str:
        """Get email alias from the config."""
        payment_gateway = payment_settings.get(self.PAYMENT_GATEWAY, '')
        payment_account = payment_settings.get(self.PAYMENT_ACCOUNT, '')
        discount = payment_settings.get(self.DISCOUNT, '')

        payment_gateway_config = self._get_payment_gateway_config(payment_gateway)
        payment_account_alias = self.get_payment_account_alias(payment_gateway, payment_account)
        discount_alias = self.get_discount_alias(payment_gateway)

        if payment_gateway and len(payment_gateway_config) == 0:
            message = f"Check 'email_alias_config.json'! Seems payment_gateway '{payment_gateway}' does not exists"
            logging.error(message)
            raise ValueError(message)

        if payment_account and len(payment_account_alias) == 0:
            message = (f"Check 'email_alias_config.json'! Seems payment_account '{payment_account}' does not exists "
                       f"in payment_gateway '{payment_gateway}'")
            logging.error(message)
            raise ValueError(message)

        if payment_account_alias:
            alias = payment_account_alias + '.'
        elif payment_gateway_config:
            alias = 'test.' + payment_gateway + self.V1 + '.'
        else:
            alias = ''

        if discount and discount_alias:
            alias += discount_alias + '.'

        logging.info(f"Email alias is {alias if len(alias) > 0 else 'empty'}")
        return alias

    def get_account_name(self, payment_settings: dict) -> str:
        """Get account name from the config according to payment_gateway and account version"""
        payment_gateway = payment_settings.get(self.PAYMENT_GATEWAY, '')
        payment_account = payment_settings.get(self.PAYMENT_ACCOUNT, '')

        # Use the first payment gateway from the config, if not specified
        if not payment_gateway:
            payment_gateway = next(iter(self.config_data.keys()), None)

        # Raise error if payment_gateway is not found in the config
        if payment_gateway not in self.config_data:
            msg = f"Check 'email_alias_config.json'! '{payment_gateway}' is not found"
            logging.error(msg)
            raise KeyError(msg)

        account_name_config = self.get_account_name_config(payment_gateway)

        # Use the first payment_account from the config, if not specified
        if not payment_account:
            payment_account = next(iter(account_name_config.keys()), None)

        # Raise error if payment_account is not found in the 'account_name' config
        if payment_account not in account_name_config:
            msg = f"Check 'email_alias_config.json'! '{payment_account}' is not found in '{self.ACCOUNT_NAME}'"
            logging.error(msg)
            raise KeyError(msg)

        return account_name_config[payment_account]
