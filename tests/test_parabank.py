USERNAME = 'testuser9'
PASSWORD = '12345qwerty9'


def test_signup_user(home_page):
    home_page.signup_user(USERNAME, PASSWORD)
    result_element = home_page.item('signup_result_title')
    assert result_element.get_text() == 'Signing up is easy!'


def test_login_with_valid_data(home_page):
    home_page.signin_user(USERNAME, PASSWORD)
    login_result = home_page.item('login_title')
    assert login_result.get_text() == 'Accounts Overview'

