# pip3 install selenium
import csv
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from utils import Utils

class CoinGeckoNftScraper:

    def __init__(self):

        self.utils = Utils()

    def parse_collection_slugs(self, page_source):

        collection_slugs = []

        soup = BeautifulSoup(page_source, features="html.parser")
        table = soup.find("div", {"class": "coingecko-table"})

        for tr in table.find_all('tr'):

            a_tag = tr.find('a', href=True)
            
            try:
                href = (a_tag['href'])
                collection_slug = href.replace('/en/nft/', '')
            except:
                href = None
                collection_slug = None

            print (collection_slug)  

            if collection_slug:
                collection_slugs.append(collection_slug)  

        return collection_slugs

    def scrape_collection_slugs(self, coingecko_page_num):

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(f"https://www.coingecko.com/en/nft?page={coingecko_page_num}")
        delay = 60
        
        # CoinGecko uses CloudFlare... wait to load page
        try:
        
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'coingecko-table'))
            WebDriverWait(driver, delay).until(element_present)
            
            page_source = driver.page_source
            driver.quit()

            collection_slugs = parse_collection_slugs(page_source)
            return collection_slugs
        
        except TimeoutException:
        
            print ("Web page taking too much time to load...")
            print ("Retry...")
            # Quit driver and try again...
            driver.quit()
            return self.scrape_collection_slugs(coingecko_page_num)

    def scrape_coingecko_nft_page_range(self, start_page_num, end_page_num):

        for page_num in np.arange(start_page_num, end_page_num + 1):
            collection_slugs = self.scrape_collection_slugs(page_num)
            self.utils.export_to_csv_file(f"data/collections_page_{page_num}.csv", collection_slugs)

if __name__ == "__main__":

    start_page_num = 4
    end_page_num = 6
    coingecko_nft_scraper = CoinGeckoNftScraper()
    coingecko_nft_scraper = coingecko_nft_scraper.scrape_coingecko_nft_page_range(start_page_num, end_page_num)