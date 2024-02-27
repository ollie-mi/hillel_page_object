import sys
import pathlib
import pytest
root = str(pathlib.Path(__file__).parent.parent)
sys.path.insert(0, root)

from pages.home_page import HomePage as HP


def test_homepage_menu(driver):
    home_page = HP(driver)
    element = home_page.item("menu_home")
    assert element.is_visible(), f"Not found: {element._locator}"
    # element.highlight_and_make_screenshot("menu_home.png")


def test_homepage_sign_in(driver):
    home_page = HP(driver)
    element = home_page.item("sign_in_button")
    assert element.is_visible(), f"Not found: {element._locator}"


def test_fail_path(driver):
    home_page = HP(driver)
    with pytest.raises(AttributeError):
        element = home_page.item("sign_in_button2")
        element.is_visible()
