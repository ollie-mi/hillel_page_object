import pytest
from globals import dir_globals
from pages.signup_page import SignUpPage


@pytest.mark.closer
@pytest.mark.signup
class TestSignupPageEvents:
    CURRENT_SCREEN = 'signup'
    NEXT_SCREEN = 'checkout-paywall'

    GISMART = 'gismart'
    EVENT_SERVICE = 'kibana'
    AMPLITUDE = 'amplitude'

    @pytest.mark.signup_events
    def test_signup_gismart_events(self, driver, user_email):
        """Test opens signup page. Verifies events that were sent before creating account"""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        screen_events_config = signup.get_screen_events_from_config(self._domain, self._landing, self.CURRENT_SCREEN,
                                                                    self.GISMART)
        screen_events = signup.get_screen_events_from_network(self._env, self._domain, self._landing,
                                                              self.CURRENT_SCREEN, self.GISMART)
        landing_type_config = signup.get_landing_type_from_config(self._domain, self._landing)

        for event in screen_events_config:
            assert event in screen_events.keys(), f"Event {event} is not found in network events"

            # Get request data from event
            request = screen_events[event]
            assert request['response_status_code'] == 200, "Wrong response status code. Should be 200"

            # Get request params from request data
            request_params = screen_events[event]['request_params']
            assert len(request_params['user_id']) != 0, "Empty 'user_id'"
            assert request_params['event_type'] == event, "Wrong 'event_type'"

            # Get event_properties from request_param
            event_properties = request_params['event_properties']
            assert event_properties['app_domain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['appDomain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['utm']['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['landing_type'] == landing_type_config['landing_type'], "Wrong 'landing_type'"
            assert event_properties['landingType'] == landing_type_config['landingType'], "Wrong 'landingType'"
            assert event_properties['app_name'] == landing_type_config['app_name'], "Wrong 'app_name'"
            assert event_properties['appName'] == landing_type_config['appName'], "Wrong 'appName'"

    @pytest.mark.signup_events
    def test_signup_gismart_events_after_creating_account(self, driver, user_email):
        """Test opens signup page and creates account. Verifies events that were sent after creating account"""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        signup.create_account(user_email)
        screen_events_config = signup.get_screen_events_from_config(self._domain, self._landing, self.NEXT_SCREEN,
                                                                    self.GISMART)
        screen_events = signup.get_screen_events_from_network(self._env, self._domain, self._landing, self.NEXT_SCREEN,
                                                              self.GISMART)
        landing_type_config = signup.get_landing_type_from_config(self._domain, self._landing)

        for event in screen_events_config:
            assert event in screen_events.keys(), f"Event {event} is not found in network events"

            # Get request data from event
            request = screen_events[event]
            assert request['response_status_code'] == 200, "Wrong response status code. Should be 200"

            # Get request params from request data
            request_params = screen_events[event]['request_params']
            assert len(request_params['user_id']) != 0, "Empty 'user_id'"
            assert request_params['event_type'] == event, "Wrong 'event_type'"

            # Get event_properties from request_param
            event_properties = request_params['event_properties']
            assert event_properties['app_domain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['appDomain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['utm']['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['landing_type'] == landing_type_config['landing_type'], "Wrong 'landing_type'"
            assert event_properties['landingType'] == landing_type_config['landingType'], "Wrong 'landingType'"
            assert event_properties['app_name'] == landing_type_config['app_name'], "Wrong 'app_name'"
            assert event_properties['appName'] == landing_type_config['appName'], "Wrong 'appName'"

    @pytest.mark.signup_events
    def test_signup_kibana_events(self, driver, user_email):
        """Test opens signup page. Verifies events that were sent before creating account"""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        screen_events_config = signup.get_screen_events_from_config(self._domain, self._landing, self.CURRENT_SCREEN,
                                                                    self.EVENT_SERVICE)
        screen_events = signup.get_screen_events_from_network(self._env, self._domain, self._landing,
                                                              self.CURRENT_SCREEN, self.EVENT_SERVICE)
        landing_type_config = signup.get_landing_type_from_config(self._domain, self._landing)

        for event in screen_events_config:
            assert event in screen_events.keys(), f"Event {event} is not found in network events"

            # Get request data from event
            request = screen_events[event]
            assert request['response_status_code'] == 200, "Wrong response status code. Should be 200"

            # Get request params from request data
            request_params = screen_events[event]['request_params']
            assert len(request_params['user_id']) != 0, "Empty 'user_id'"
            assert request_params['event_type'] == event, "Wrong 'event_type'"

            # Get event_properties from request_param
            event_properties = request_params['event_properties']
            assert event_properties['app_domain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['appDomain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['utm']['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['landing_type'] == landing_type_config['landing_type'], "Wrong 'landing_type'"
            assert event_properties['landingType'] == landing_type_config['landingType'], "Wrong 'landingType'"
            assert event_properties['app_name'] == landing_type_config['app_name'], "Wrong 'app_name'"
            assert event_properties['appName'] == landing_type_config['appName'], "Wrong 'appName'"

    @pytest.mark.signup_events
    def test_signup_kibana_events_after_creating_account(self, driver, user_email):
        """Test opens signup page and creates account. Verifies events that were sent after creating account"""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        signup.create_account(user_email)
        screen_events_config = signup.get_screen_events_from_config(self._domain, self._landing, self.NEXT_SCREEN,
                                                                    self.EVENT_SERVICE)
        screen_events = signup.get_screen_events_from_network(self._env, self._domain, self._landing, self.NEXT_SCREEN,
                                                              self.EVENT_SERVICE)
        landing_type_config = signup.get_landing_type_from_config(self._domain, self._landing)

        for event in screen_events_config:
            assert event in screen_events.keys(), f"Event {event} is not found in network events"

            # Get request data from event
            request = screen_events[event]
            assert request['response_status_code'] == 200, "Wrong response status code. Should be 200"

            # Get request params from request data
            request_params = screen_events[event]['request_params']
            assert len(request_params['user_id']) != 0, "Empty 'user_id'"
            assert request_params['event_type'] == event, "Wrong 'event_type'"

            # Get event_properties from request_param
            event_properties = request_params['event_properties']
            assert event_properties['app_domain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['appDomain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['utm']['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['landing_type'] == landing_type_config['landing_type'], "Wrong 'landing_type'"
            assert event_properties['landingType'] == landing_type_config['landingType'], "Wrong 'landingType'"
            assert event_properties['app_name'] == landing_type_config['app_name'], "Wrong 'app_name'"
            assert event_properties['appName'] == landing_type_config['appName'], "Wrong 'appName'"

    @pytest.mark.signup_events
    def test_signup_amplitude_events(self, driver, user_email):
        """Test opens signup page. Verifies events that were sent before creating account"""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        screen_events_config = signup.get_screen_events_from_config(self._domain, self._landing, self.CURRENT_SCREEN,
                                                                    self.AMPLITUDE)
        screen_events = signup.get_screen_events_from_network(self._env, self._domain, self._landing,
                                                              self.CURRENT_SCREEN, self.AMPLITUDE)

        assert len(screen_events_config) == 0, f"Amplitude config for the page '{self.CURRENT_SCREEN}' is not empty"
        assert len(screen_events) == 0, f"Amplitude network events for the page '{self.CURRENT_SCREEN}' are detected"

    @pytest.mark.signup_events
    def test_signup_amplitude_events_after_creating_account(self, driver, user_email):
        """Test opens signup page and creates account. Verifies events that were sent after creating account"""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        signup.create_account(user_email)
        screen_events_config = signup.get_screen_events_from_config(self._domain, self._landing, self.NEXT_SCREEN,
                                                                    self.AMPLITUDE)
        screen_events = signup.get_screen_events_from_network(self._env, self._domain, self._landing, self.NEXT_SCREEN,
                                                              self.AMPLITUDE)
        landing_type_config = signup.get_landing_type_from_config(self._domain, self._landing)

        for event in screen_events_config:
            assert event in screen_events.keys(), f"Event {event} is not found in network events"

            # Get request data from event
            request = screen_events[event]
            assert request['response_status_code'] == 200, "Wrong response status code. Should be 200"

            # Get request params from request data
            request_params = screen_events[event]['request_params']
            assert len(request_params['user_id']) != 0, "Empty 'user_id'"
            assert request_params['event_type'] == event, "Wrong 'event_type'"

            # Get event_properties from request_param
            event_properties = request_params['event_properties']
            assert event_properties['app_domain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['appDomain'] == self._base_url.rstrip('/'), "Wrong domain url"
            assert event_properties['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['utm']['utm_source'] == dir_globals.UTM_SOURCE, "Wrong utm_source"
            assert event_properties['landing_type'] == landing_type_config['landing_type'], "Wrong 'landing_type'"
            assert event_properties['landingType'] == landing_type_config['landingType'], "Wrong 'landingType'"
            assert event_properties['app_name'] == landing_type_config['app_name'], "Wrong 'app_name'"
            assert event_properties['appName'] == landing_type_config['appName'], "Wrong 'appName'"
