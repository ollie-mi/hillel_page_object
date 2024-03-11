from globals import dir_globals
from config_parsers.config_url_parser import ConfigOnboardingUrlParser


class CloserOnboardingUrlParser(ConfigOnboardingUrlParser):
    """ Parses Closer Onboarding urls"""

    def __init__(self):
        super().__init__(dir_globals.CLOSER_ONBOARDING_URLS)
