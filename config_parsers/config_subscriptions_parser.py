import json
import logging


class SubscriptionConfigParser:
    """ Parses config with subscriptions for specific onboarding
    """
    SUBSCRIPTION_PLANS = 'subscription_plans'
    COUPONS = 'coupons'
    UPSELL_PLANS = 'upsell_plans'

    def __init__(self, subscriptions_list_path, onboarding_subscriptions_path):
        self.subscriptions_list = self._load_config_data(subscriptions_list_path)
        self.onboarding_subscriptions = self._load_config_data(onboarding_subscriptions_path)

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

    def _get_subscription_by_id(self, subscription_id: str) -> dict:
        """Get event name from even list config"""
        return self.subscriptions_list.get(self.SUBSCRIPTION_PLANS, {}).get(subscription_id, {})

    def _get_coupon_by_id(self, coupon_id: str) -> dict:
        """Get event name from even list config"""
        return self.subscriptions_list.get(self.COUPONS, {}).get(coupon_id, {})

    def _get_upsell_by_id(self, upsell_id: str) -> dict:
        """Get event name from even list config"""
        return self.subscriptions_list.get(self.UPSELL_PLANS, {}).get(upsell_id, {})

    def get_onboarding_subscriptions_amount(self, domain: str, landing: str) -> int:
        """Get amount of subscriptions for specific onboarding"""
        if len(landing) == 0:
            landing = 'default'
        plans_list = self.onboarding_subscriptions.get(domain, {}).get(landing, {}).get(self.SUBSCRIPTION_PLANS, [])
        if len(plans_list) == 0:
            message = f"Plans are not configured for domain: {domain}, landing: {landing}"
            logging.error(message)
            raise ValueError(message)
        return len(plans_list)


