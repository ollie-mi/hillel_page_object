import pytest
from get_browser import firefox, chrome

from pages.home_page import HomePage

URL = "https://guest:welcome2qauto@qauto.forstudy.space/"

@pytest.fixture(scope="module")
def driver():
    _driver = firefox()
    _driver.maximize_window()
    _driver.get(URL)
    yield _driver
    _driver.quit()

@pytest.fixture
def home_page(driver):
    return HomePage(driver)

