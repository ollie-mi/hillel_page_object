import pytest
from pages.signup_page import SignUpPage
from closer_configs.expected_pages_config_parser import CloserExpectedPagesConfigParser


@pytest.mark.closer
@pytest.mark.signup
class TestSignupPage:
    CURRENT_SCREEN = 'signup'
    expected_pages = CloserExpectedPagesConfigParser()

    @pytest.mark.signup_ui
    def test_create_account_with_valid_email(self, driver, user_email):
        """Test opens signup page and creates account. Verifies that checkout page opens."""
        signup = SignUpPage(driver, self._base_url)
        signup.open_signup_page(self._domain_url)
        signup.create_account(user_email)

        expected_page = self.expected_pages.get_expected_next_page(self._domain, self._landing, self.CURRENT_SCREEN)
        expected_url = self._domain_url + expected_page

        current_url = signup.get_current_url()

        assert current_url == expected_url, f"Wrong expected url {expected_url}. Current url: {current_url}"
