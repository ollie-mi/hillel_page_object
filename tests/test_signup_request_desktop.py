import logging
import pytest
from pages.signup_page import SignUpPage
from closer_configs.email_alias_parser import CloserEmailAlias
from closer_configs.expected_pages_config_parser import CloserExpectedPagesConfigParser


@pytest.mark.closer
@pytest.mark.signup
class TestSignupPageRequest:
    CURRENT_SCREEN = 'signup'
    expected_pages = CloserExpectedPagesConfigParser()
    payment_settings_config = CloserEmailAlias()

    @pytest.mark.signup_request
    def test_signup_request(self, driver, user_email):
        """Test opens signup page and creates account. Verifies signup request."""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        signup.create_account(user_email)
        request_data = signup.get_signup_request_from_network()

        # get actual data from response
        signup_request = request_data[0]
        actual_status_code = signup_request.get('response_status_code')
        actual_user_uuid = signup_request.get('request_body').get('user_uuid')
        logging.info(f"'user_uuid' is {actual_user_uuid}")
        signup_response_body = signup_request.get('response_body').get('data').get('entity')
        actual_registration_source = signup_response_body.get('registration_source')
        actual_name = signup_response_body.get('name')
        actual_email = signup_response_body.get('email')
        actual_id = signup_response_body.get('id')
        logging.info(f"User 'id' is {actual_id}")
        actual_external_user_id = signup_response_body.get('external_user_id')
        logging.info(f"'external_user_id' is {actual_external_user_id}")

        assert len(request_data) == 1, "Wrong amount of requests"
        assert actual_status_code == 201, f"Wrong response status_code. Should be 201. Received {actual_status_code}"

        assert actual_registration_source == 'email', (f"Wrong registration_source. Should be 'email'. "
                                                       f"Received {actual_registration_source}")
        assert actual_name == user_email, f"Wrong 'name'. Should be {user_email}. Received {actual_name}"
        assert actual_email == user_email, f"Wrong 'name'. Should be {user_email}. Received {actual_email}"

        assert actual_id is not None, "id is empty"
        assert actual_external_user_id is not None, "external_user_id is empty"

    @pytest.mark.signup_payment_settings
    def test_signup_payment_settings_request(self, driver, user_email, parse_addoption_payment_settings):
        """Test opens signup page and creates account. Verifies signup payment-settings request."""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        signup.create_account(user_email)
        request_data = signup.get_payment_settings_request_from_network()

        # get actual data from response
        payment_settings_request = request_data[0]
        actual_status_code = payment_settings_request.get('response_status_code')
        payment_settings_response_body = payment_settings_request.get('response_body')
        actual_stripe_account_name = payment_settings_response_body.get('stripe_account_name')
        actual_stripe_publishable_key = payment_settings_response_body.get('stripe_publishable_key')

        expected_account_name = self.payment_settings_config.get_account_name(parse_addoption_payment_settings)

        assert len(request_data) == 1, "Wrong amount of requests"
        assert actual_status_code == 200, f"Wrong response status_code. Should be 200. Received {actual_status_code}"

        assert actual_stripe_account_name == expected_account_name, (f"Wrong stripe account name. "
                                                                     f"Should be {expected_account_name}. "
                                                                     f"Received {actual_stripe_account_name}")
        assert actual_stripe_publishable_key != '' "Wrong stripe publishable key. Shouldn't be empty"
