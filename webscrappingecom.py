from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'PS5'
CURRENCY = '₹'
MIN_PRICE = "30000"
MAX_PRICE = '60000'
FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}
BASE_URL = "http://www.amazon.in/"

def get_chrome_web_driver(options):
    return webdriver.Chrome(options)

def get_web_driver_options():
    return webdriver.ChromeOptions()

def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-error')

def set_browser_as_incognito(options):
    options.add_argument('--incognito')