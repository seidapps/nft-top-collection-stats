import csv
import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from dataclasses import dataclass, asdict
from datetime import datetime
from bs4 import BeautifulSoup

@dataclass
class OpenseaCollection:
    rank_num: int
    collection_slug: str
    created_date: str
    num_owners: int
    floor_price: float
    total_volume: str
    total_supply: str
    thirty_day_volume: float
    thirty_day_change: float

class OpenseaRankingsScraper:

    def parse_rankings_html(self, page_source):

        soup = BeautifulSoup(page_source, "html.parser")

        rankings = []
        scripts = soup.find_all('script')
        for script in scripts:

            # TODO: update this...
            # Currently identifying target script elements through a popular collection slug
            # GraphQL json is within second / last script element
            if 'mutant-' in str(script):
                json_data = script.text
                rankings.append(json_data)

        collections = json.loads(str(rankings[-1]))

        output_filename = 'data/rankings_{}.csv'.format(datetime.now().strftime("%Y%m%d"))
        with open(output_filename, 'w') as f:

            writer = csv.DictWriter(f, fieldnames=list(OpenseaCollection.__annotations__.keys()))
            writer.writeheader()

            edges = collections['props']['relayCache'][0][1]['json']['data']['rankings']['edges']
            for rank_num, edge in enumerate(edges):

                node = edge['node']
                stats = node['statsV2']

                floor_price_base = stats.get('floorPrice', None)
                if floor_price_base is not None:
                    floor_price = floor_price_base.get('eth', None)

                collection_stats = OpenseaCollection(
                    rank_num = rank_num,
                    collection_slug = node['slug'],
                    created_date = node['createdDate'],
                    num_owners = stats['numOwners'],
                    floor_price = floor_price,
                    total_volume = stats['totalVolume']['unit'],
                    total_supply = stats['totalSupply'],
                    thirty_day_volume = stats['thirtyDayVolume']['unit'],
                    thirty_day_change = stats['thirtyDayChange']
                )

                writer.writerow(asdict(collection_stats))

    def scrape_collection_rankings(self):

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://opensea.io/rankings")
        delay = 30
        
        try:

            element_present = EC.presence_of_element_located((By.ID, '__next'))
            WebDriverWait(driver, delay).until(element_present)            
            page_source = driver.page_source

            self.parse_rankings_html(page_source)

        except TimeoutException:
            print ("Web page taking too much time to load...")
        finally:
            driver.quit()

if __name__ == "__main__":

    opensea_rankings_scraper = OpenseaRankingsScraper()
    opensea_rankings_scraper.scrape_collection_rankings()