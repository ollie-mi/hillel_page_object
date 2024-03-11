from globals import dir_globals
from config_parsers.config_onboarding_events_parser import OnboardingEventsConfigParser


class CloserOnboardingEventsConfigParser(OnboardingEventsConfigParser):
    """ Parses config with events for every page of onboarding
    """

    def __init__(self):
        super().__init__(dir_globals.CLOSER_EVENTS_LIST_CONFIG, dir_globals.CLOSER_ONBOARDING_EVENTS_CONFIG)
