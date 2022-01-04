from dataclasses import dataclass
import json
import numpy as np

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

from utils import Utils

@dataclass
class OpenseaCollection:
    collection_slug: str
    created_date: str
    market_cap: float
    num_owners: int
    floor_price: float
    total_volume: str
    total_supply: str
    thirty_day_volume: float
    thirty_day_change: float

class OpenseaRankingsScraper:

    def __init__(self):

        self.utils = Utils()

    def parse_rankings_html(self, page_source):

        # import codecs
        # f = codecs.open("page.html", 'r')
        # page_source = f.read()

        soup = BeautifulSoup(page_source, "html.parser")
        scripts = soup.find_all('script')
        for script in scripts:

            if 'mutant-' in str(script):
                json_data = script.text

        collections = json.loads(str(json_data))

        edges = collections['props']['relayCache'][0][1]['json']['data']['rankings']['edges']

        for edge in edges:

            node = edge['node']
            stats = node['stats']

            collection_stats = OpenseaCollection(
                collection_slug = node['slug'],
                created_date = node['createdDate'],
                market_cap = stats['marketCap'],
                num_owners = stats['numOwners'],
                floor_price = node['floorPrice'],
                total_volume = stats['totalVolume'],
                total_supply = stats['totalSupply'],
                thirty_day_volume = stats['thirtyDayVolume'],
                thirty_day_change = stats['thirtyDayChange']
            )

            print (collection_stats)

    def scrape_collection_rankings(self):

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://opensea.io/rankings")
        delay = 30
        
        # CoinGecko uses CloudFlare... wait to load page
        try:
        
            element_present = EC.presence_of_element_located((By.ID, '__next'))
            WebDriverWait(driver, delay).until(element_present)
            
            page_source = driver.page_source
            driver.quit()

            self.parse_rankings_html(page_source)

            # html_file= open("page.html","w")
            # html_file.write(str(page_source))
            # html_file.close()

            # print (page_source)

            driver.quit()

        except TimeoutException:
        
            print ("Web page taking too much time to load...")
            print ("Retry...")
            # Quit driver and try again...
            driver.quit()

if __name__ == "__main__":

    opensea_rankings_scraper = OpenseaRankingsScraper()
    opensea_rankings_scraper.scrape_collection_rankings()