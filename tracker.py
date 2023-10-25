from webscrappingecom import(get_chrome_web_driver,get_web_driver_options,set_browser_as_incognito,set_ignore_certificate_error,NAME,CURRENCY,FILTERS,BASE_URL,DIRECTORY)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

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
        pass

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


        def get_products_info(self, links):
            asins = self.get_asins(links)
            products = []
            for asins in asins:
                product = self.get_single_product_info(asins)

        def get_single_product_info(self, asin):
            print("Product ID: {asin} - getting data...")
            product_short_url = self.shorten_url(asin) 
            self.driver.get(f'{product_short_url}')
            title = self.get_title()
            seller = self.get_seller()
            price = self.get_price()

        def get_title(self):
            try:
                return self.driver.find_elemnt('id', 'productTitle').text
            except Exception as e:
                print(e)
                print(f'Cant get title of a product - {self.driver.current_}')
                return None

        def get_seller(self):
            try:
                return self.driver.find_element('id', 'bylineInfo' ).text
            except Exception as e:
                print(e)
                print(f"Can't get seller of a product" - {self.driver.current_url})
                return None

        def get_price(self):
            return '99$'

        def shorten_url(self, asin):
            return self.base_url + 'dp/' + asin

        def get_asins(self, links):
            return  [self.get_asins(link) for link in links]

        def get_asins(self, asin):
            return product_links[product_link.find('/dp/')+ 4:product_link.find('/ref')]
        

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element("id", 'twotabsearchtextbox')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}') 
        result_list = self.driver.find_element(By.CLASS_NAME, 's-result-list')
        
        links = []
        try:
            results = result_list[0].find_elements('xpath', "//div[1]/div[1]/div[1]/div[1]/div[1]/span[1]/div[1]/div[2]/div[1]")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didnt get any products")
            print(e)
            return links



if __name__ == '__main__':
    print("Heyy")
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    print(amazon.price_filter)
    amazon.run()