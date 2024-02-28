from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    locators = dict(
        menu_home='//a[text()="Home"]',
        sign_in_button='//button[.="Sign In"]',
        contacts_head='//h2',
        sign_up_button='//button[.="Sign Up"]'
        )
