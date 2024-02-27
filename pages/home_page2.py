from pages.elements import WebElement
from pages.base_page import BasePage


class HomePage(BasePage):

    locators = dict(
        menu_home = '//a[text()="Home"]',
        sign_in_button = '//button[.="Sign In"]',
        contacts_head = '//h2',
        sign_up_button = '//button[.="Sign Up"]'
        )

    def __init__(self, driver):
        super().__init__(driver)

    def item(self, name:str):
        _xpath = self.locators.get(name)
        if _xpath is None:
            raise AttributeError(
                f"{self.__class__.__name__} has no xpath for element: {name}, " \
                f"may be typo? Exsist names is: {self.locators.keys()}"
                )
        return WebElement(driver=self.driver, xpath=_xpath)
