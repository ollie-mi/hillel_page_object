import time

from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    locators = dict(
        menu_home='//a[text()="Home"]',
        sign_in_button='//button[.="Sign In"]',
        contacts_head='//h2',
        sign_up_button='//button[.="Sign Up"]',
        username_by='//[@name="email"]',
        password_by="password",
        signin_by='//form//div[.="Login"]',
        username_input='//input[@name="username"]',
        password_input='//input[@name="password"]',
        login_button='//*[@id="loginPanel"]/form/div[3]/input',
        register_link='//*[@id="loginPanel"]/p[2]/a',
        first_name='//input[@id="customer.firstName"]',
        last_name='//input[@id="customer.lastName"]',
        address='//input[@id="customer.address.street"]',
        city='//input[@id="customer.address.city"]',
        state='//input[@id="customer.address.state"]',
        zip_code='//input[@id="customer.address.zipCode"]',
        phone_number='//input[@id="customer.phoneNumber"]',
        ssn='//input[@id="customer.ssn"]',
        username='//input[@id="customer.username"]',
        password='//input[@id="customer.password"]',
        repeat_password='//input[@id="repeatedPassword"]',
        register_button='//*[@id="customerForm"]/table/tbody/tr[13]/td[2]/input',
        signup_result_title='//*[@id="rightPanel"]/h1',
        signup_result_p='//*[@id="rightPanel"]/p',
        login_title='//*[@id="rightPanel"]/div/div/h1'
        )

    def login_valid_user(self, username, password):
        username_by = self.item("username_by")
        password_by = self.item("password_by")
        signin_by = self.item("signin_by")

        username_by.send_keys(username)
        password_by.send_keys(password)
        signin_by.click()

    def signin_user(self, username, password):
        username_element = self.item("username_input")
        username_element.send_keys(username)
        password_element = self.item("password_input")
        password_element.send_keys(password)

        login_button = self.item("login_button")
        login_button.click()

    def open_signup_page(self):
        element = self.item("register_link")
        element.click()

    def signup_user(self, username_data, password_data):
        self.open_signup_page()
        first_name = self.item("first_name")
        first_name.send_keys("Test")
        last_name = self.item("last_name")
        last_name.send_keys("Test")
        addr = self.item("address")
        addr.send_keys("Some street, 23")
        city = self.item("city")
        city.send_keys("Kyiv")
        state = self.item("state")
        state.send_keys("Kyiv")
        zip_code = self.item("zip_code")
        zip_code.send_keys("12345")
        phone = self.item("phone_number")
        phone.send_keys("380631112233")
        ssn = self.item("ssn")
        ssn.send_keys('12345')

        username = self.item("username")
        username.send_keys(username_data)
        password = self.item("password")
        password.send_keys(password_data)
        repeat_password = self.item("repeat_password")
        repeat_password.send_keys(password_data)

        register_button = self.item("register_button")
        register_button.click()
