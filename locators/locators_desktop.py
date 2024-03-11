from selenium.webdriver.common.by import By

CONTINUE_BUTTON = (By.XPATH, '//*[@id="continue-button"]')
SIGN_UP_INPUT = (By.XPATH, '//*[@id="sign-up-input"]')
PLAN_BUTTON_1 = (By.XPATH, '//*[@id="plan-button-1"]')
PLAN_BUTTON_2 = (By.XPATH, '//*[@id="plan-button-2"]')
PLAN_BUTTON_3 = (By.XPATH, '//*[@id="plan-button-3"]')
COME_BACK_BUTTON = (By.XPATH, '//*[@id="come-back-button"]')
CARD_NUMBER_IFRAME = (By.XPATH, '//div[@id="card-number-element"]//iframe[1]')
CARD_NUMBER_ELEMENT = (By.XPATH, '//input[@name="cardnumber" or @name="credit-card-number"]')
CARD_EXPIRY_IFRAME = (By.XPATH, '//div[@id="card-expiry-element"]//iframe[1]')
CARD_EXPIRY_ELEMENT = (By.XPATH, '//input[@name="exp-date" or @name="expiration"]')
CARD_CVV_IFRAME = (By.XPATH, '//div[@id="card-cvc-element"]//iframe[1]')
CARD_CVV_ELEMENT = (By.XPATH, '//input[@name="cvc" or @name="cvv"]')
CARDHOLDER_NAME_ELEMENT = (By.XPATH, '//*[@id="cardholder-name-element"]')
LOADING_ELEMENT = (By.XPATH, '//*[@id="loading-element"]')
IFRAME = (By.XPATH, '//iframe')
STRIPE_3DS_IFRAME = (By.XPATH, '//iframe[@id="challengeFrame"]')
STRIPE_3DS_CONFIRM_BUTTON = (By.XPATH, '//button[@id="test-source-authorize-3ds"]')
