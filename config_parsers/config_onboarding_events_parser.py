import json
import logging


class OnboardingEventsConfigParser:
    """ Parses config with events for every page of onboarding
    """
    EVENT_LIST = 'events_by_id'

    def __init__(self, event_list_path, onboarding_events_path):
        self.events_list = self._load_config_data(event_list_path)
        self.onboarding_events = self._load_config_data(onboarding_events_path)

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

    def _get_event_by_id(self, event_id: str) -> str:
        """Get event name from even list config"""
        return self.events_list.get(self.EVENT_LIST, {}).get(event_id, '')

    def get_screen_event_list(self, domain: str, landing: str, screen: str, analytic_system: str) -> list:
        """Get expected events for the specific screen"""
        if len(landing) == 0:
            landing = 'default'
        domain_events_config = self.onboarding_events.get(domain, {})
        landing_events_config = domain_events_config.get(landing, {})

        if landing_events_config is None:
            message = f"No events configured for domain: {domain}, landing: {landing}"
            logging.error(message)
            raise ValueError(message)

        screen_event_config = landing_events_config.get(screen, {})
        event_data = screen_event_config.get(analytic_system)

        if event_data is None:
            message = (f"No events configured for domain: {domain}, landing: {landing}, screen: {screen}, "
                       f"analytic_system: {analytic_system}")
            logging.error(message)
            raise ValueError(message)

        result = []
        for event in event_data:
            event_name = self._get_event_by_id(str(event))
            if not event_name:
                message = f"Event id {event} is not found in event list config"
                logging.error(message)
                raise ValueError(message)
            result.append(event_name)
        logging.info("Event list for the screen is received")
        return result
