import pytest
from get_browser import firefox, chrome

from pages.home_page import HomePage

URL = "https://parabank.parasoft.com/parabank/index.htm"

@pytest.fixture(scope="function")
def driver():
    _driver = firefox(True)
    _driver.maximize_window()
    _driver.get(URL)
    yield _driver
    _driver.quit()

@pytest.fixture
def home_page(driver):
    return HomePage(driver)
