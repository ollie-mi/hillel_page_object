import sys
import pathlib
root = str(pathlib.Path(__file__).parents[2])
sys.path.insert(0, root)

from lesson_27_pt2.pages.home_page import HomePage as HP
from lesson_27_pt2.pages.home_page2 import HomePage as HP2

def test_homepage_menu(driver):
    home_page = HP(driver)
    element = home_page.menu_home()
    assert element.is_visible(), f"Not found: {element._locator}"
    element.highlight_and_make_screenshot("menu_home.png")

def test_homepage_sign_in(driver):
    home_page = HP2(driver)
    element = home_page.item("sign_in_button")
    assert element.is_visible(), f"Not found: {element._locator}"

def test_homepage_sign_in2(driver):
    home_page = HP2(driver)
    element = home_page.item("sign_in_button2")
    assert element.is_visible(), f"Not found: {element._locator}"

