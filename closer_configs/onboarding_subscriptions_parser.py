from globals import dir_globals
from config_parsers.config_subscriptions_parser import SubscriptionConfigParser


class CloserSubscriptionConfigParser(SubscriptionConfigParser):
    """ Parses config with subscriptions for specific onboarding
        """

    def __init__(self):
        super().__init__(dir_globals.CLOSER_SUBSCRIPTION_LIST_CONFIG, dir_globals.CLOSER_ONBOARDING_SUBSCRIPTIONS_CONFIG)