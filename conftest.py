import pytest
from get_browser import firefox, chrome

URL = "https://guest:welcome2qauto@qauto.forstudy.space/"

@pytest.fixture(scope="module")
def driver():
    _driver = firefox()
    _driver.maximize_window()
    _driver.get(URL)
    yield _driver
    _driver.quit()
