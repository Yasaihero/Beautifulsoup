from webscrappingecom import (
    get_chrome_web_driver,
    get_web_driver_options,
    set_browser_as_incognito,
    set_ignore_certificate_error,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY,
)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting script...")
        print(f"Looking for {self.search_term} products...")
        links = self.get_products_links()
        if not links:
            print("Stopped script.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting information about products...")
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 's-result-list')))
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        result_list = self.driver.find_element(By.CLASS_NAME, 's-result-list')

        links = []
        try:
            results = result_list.find_elements(By.XPATH, "//div/span/div/div//h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didnt get any products")
            print(e)
            return links

    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            products.append(product)
        return products

    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(product_short_url)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()

    def get_title(self):
        try:
            return self.driver.find_element(By.ID, 'productTitle').text
        except Exception as e:
            print(e)
            print(f"Cant get title of a product - {self.driver.current_url}")
            return None

    def get_seller(self):
        try:
            return self.driver.find_element(By.ID, 'bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of a product - {self.driver.current_url}")
            return None

    def get_price(self):
        return '£99'

    def shorten_url(self, asin):
        return self.base_url + 'dp/' + asin

    def get_asins(self, links):
        return [self.get_asin(link) for link in links]

    def get_asin(self, link):
        return link[link.find('/dp/') + 4:link.find('/ref')]

if __name__ == '__main__':
    print("Heyy")
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    print(amazon.price_filter)
    amazon.run()
