import logging
import pytest
from distutils.util import strtobool
from config_parsers.config_analytics_systems_url_parser import ConfigAnalyticsSystemsUrlParser
from helpers.helpers import generate_user_email
from closer_configs.config_url_parser import CloserOnboardingUrlParser
from closer_configs.email_alias_parser import CloserEmailAlias
from closer_configs.onboarding_subscriptions_parser import CloserSubscriptionConfigParser
from portpicker import pick_unused_port
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

SELENIUM_HUB_URL = 'http://127.0.0.1:4444/wd/hub'

BROWSER_DRIVERS = {
    'firefox': (webdriver.Firefox, webdriver.FirefoxOptions, FirefoxService, GeckoDriverManager, None),
    'edge': (webdriver.Edge, webdriver.EdgeOptions, EdgeService, EdgeChromiumDriverManager, None),
    'safari': (webdriver.Safari, None, None, None, {'port': 9090}),
    'chrome': (webdriver.Chrome, webdriver.ChromeOptions, ChromeService, ChromeDriverManager, None)
}


def pytest_addoption(parser):
    """Reads parameters from pytest command line"""
    parser.addoption("--env", action="store", default="stage", help="Type environment: 'stage' or 'prod'")
    parser.addoption("--domain", action="store", default="quiz", help="Type of onboarding domain: 'quiz', 'pairs'..")
    parser.addoption("--landing", action="store", default="", help="Type of onboarding landing: 'bravo', 'testb' ..")
    parser.addoption("--payment_gateway", action="store", default="", help="Choose 'stripe' or 'braintree'")
    parser.addoption("--payment_account", action="store", default="",
                     help="Choose 'stripe' or 'braintree' payment account: v1, v2, v3, uk1")
    parser.addoption("--browser", action="store", default="chrome", help="Choose browser: 'chrome', 'firefox', "
                                                                         "'edge', 'safari'")
    parser.addoption("--remote", action="store", default="True", help="True for Selenium hub and False for local run")


@pytest.fixture(scope="class", autouse=True)
def parse_addoption_base_url(request) -> dict:
    """Get onboarding parameters from pytest command line"""
    env = request.config.getoption('env').lower()
    domain = request.config.getoption('domain').lower()
    landing = request.config.getoption('landing').lower()
    parameters = {
        'env': env,
        'domain': domain,
        'landing': landing
    }
    request.cls._env = env
    request.cls._domain = domain
    request.cls._landing = landing
    return parameters


@pytest.fixture(autouse=True, scope='class')
def domain_name_url(request, parse_addoption_base_url):
    config_parser = CloserOnboardingUrlParser()
    domain_url = config_parser.get_domain_url(parse_addoption_base_url)
    request.cls._domain_url = domain_url


@pytest.fixture(scope="function")
def parse_addoption_payment_settings(request) -> dict:
    """Get payment-settings parameters from pytest command line"""
    parameters = {
        'payment_gateway': request.config.getoption('payment_gateway').lower(),
        'payment_account': request.config.getoption('payment_account').lower()
    }
    return parameters


@pytest.fixture(scope="session")
def remote(request):
    remote = bool(strtobool(request.config.getoption('remote')))
    if not isinstance(remote, bool):
        remote = True
    return remote


@pytest.fixture(autouse=True, scope='class')
def browser(request, remote) -> str:
    """Get browser parameter from pytest command line"""
    browser = request.config.getoption('browser').lower()
    if remote:
        keys_to_delete = ['edge', 'safari']
        for key in keys_to_delete:
            if key in BROWSER_DRIVERS:
                del BROWSER_DRIVERS[key]
    if browser not in BROWSER_DRIVERS.keys():
        browser = 'chrome'
    return browser


@pytest.fixture(scope="function")
def user_email(request, parse_addoption_payment_settings) -> str:
    """Get user email according to payment system"""
    alias = CloserEmailAlias().get_email_alias_by_payment_gateway(parse_addoption_payment_settings)
    email = generate_user_email()
    email = alias + email
    logging.info(f"Generate user_email: {email}")
    return email


@pytest.fixture(scope="function")
def user_discount_email(request, parse_addoption_payment_settings) -> str:
    """Get user email according to payment system"""
    parse_addoption_payment_settings['discount'] = True
    alias = CloserEmailAlias().get_email_alias_by_payment_gateway(parse_addoption_payment_settings)
    email = generate_user_email()
    email = alias + email
    logging.info(f"Generate user_email: {email}")
    return email


@pytest.fixture(scope="class", autouse=True)
def base_url(request, parse_addoption_base_url):
    """Get onboarding url from config"""
    config_parser = CloserOnboardingUrlParser()
    logging.info("Get onboarding url from config")
    url = config_parser.get_onboarding_url(parse_addoption_base_url)
    request.cls._base_url = url
    return url


@pytest.fixture(scope="function", params=[1, 2, 3])
def subscription_plan(request):
    config_parser = CloserSubscriptionConfigParser()
    config_data = config_parser.get_onboarding_subscriptions_amount(request.cls._domain, request.cls._landing)
    config_plan_list = list(range(1, config_data + 1))
    if request.param not in config_plan_list:
        pytest.skip(f"Onboarding does not have {request.param} subscription")
    return request.param


@pytest.fixture(scope="function", autouse=True)
def driver(request, browser, remote):
    """Initialize driver for testing"""
    driver_class, options_class, service_class, driver_manager, seleniumwire_options = (
        BROWSER_DRIVERS.get(browser.lower(), (None, None, None, None, None)))

    if driver_class is None:
        raise ValueError(f"Unsupported browser '{browser}'")

    service = service_class(driver_manager().install()) if service_class and not remote else None
    options = options_class() if options_class else {}

    if remote:
        # select random available port
        port = pick_unused_port()
        logging.info(f"Port is {port}")

        # setup proxy server for Chrome browser
        options.add_argument(f'--proxy-server=host.docker.internal:{port}')
        options.add_argument('--ignore-certificate-errors')

        # setup proxy server for Firefox browser
        proxy = webdriver.Proxy()
        proxy.http_proxy = f'host.docker.internal:{port}'
        proxy.https_proxy = f'host.docker.internal:{port}'
        proxy.ssl_proxy = f'host.docker.internal:{port}'
        options.proxy = proxy

        seleniumwire_options = {
            'auto_config': False,
            'port': port,
            'addr': '0.0.0.0'
        }

        driver = webdriver.Remote(
            command_executor=SELENIUM_HUB_URL,
            options=options,
            seleniumwire_options=seleniumwire_options
        )
        logging.info("Init Remote driver")
    else:
        driver = driver_class(service=service, seleniumwire_options=seleniumwire_options)
        logging.info("Init Local driver")

    # collect only analytic requests
    config_parser = ConfigAnalyticsSystemsUrlParser()
    driver.scopes = config_parser.get_all_network_requests_urls()

    driver.maximize_window()
    yield driver

    driver.quit()
