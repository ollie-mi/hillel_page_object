from globals import dir_globals
from config_parsers.config_landing_type_parser import OnboardingLandingTypeConfigParser


class CloserOnboardingLandingTypeConfigParser(OnboardingLandingTypeConfigParser):
    """ Parses config with landing types and app names for every page of onboarding
    """

    def __init__(self):
        super().__init__(dir_globals.CLOSER_LANDING_TYPES_LIST_CONFIG,
                         dir_globals.CLOSER_ONBOARDING_LANDING_TYPES_CONFIG)
