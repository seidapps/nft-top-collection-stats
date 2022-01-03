import time
import requests
import os

from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

@dataclass
class OpenseaCollection:
    collection_slug: str
    created_date: str
    market_cap: float
    num_owners: int
    floor_price: float
    total_volume: str
    total_sales: str
    total_supply: str
    thirty_day_volume: float
    thirty_day_change: float
    thirty_day_sales: float
    thirty_day_average_price: float

class OpenseaCollectionStats():

    def __init__(self):

        load_dotenv(find_dotenv())
        self.OPENSEA_API_KEY = os.getenv("OPENSEA_API_KEY")               

    def _make_request(
        self, 
        url=None,
        params=None, 
        return_response=False
    ):

        headers = {"Accept": "application/json", "X-API-KEY": self.OPENSEA_API_KEY}
        response = requests.get(url, params=params, headers=headers)

        # Successful response!
        if response.status_code == 200:
            return response.json()

        #The HTTP 429 Too Many Requests response status code indicates the 
        # user has sent too many requests in a given amount of time
        elif response.status_code == 429:
            print ("Sleeping 120 seconds and trying again...")
            time.sleep(120)            
            return self.make_request(url, params, return_response) 

        # The HyperText Transfer Protocol (HTTP) 400 Bad Request response 
        # status code indicates that the server cannot or will not process 
        # the request due to something that is perceived to be a client error 
        # (e.g., malformed request syntax, invalid request message 
        # framing, or deceptive request routing).
        if response.status_code == 400:
            raise ValueError(response.text)

        # A 504 Gateway Timeout Error means your web server didn't 
        # receive a timely response from another server upstream 
        # when it attempted to load one of your web pages.            
        elif response.status_code == 504:
            print ("The server reported a gateway time-out error.")        
            return None
        
        # Error for internal server error
        # Most likely means someone has too much activity
        elif response.status_code == 500:
            return None            

        else:
            print (response)
            print (response.status_code)         

    def parse_collection(self, response_json):

        collection = response_json['collection']
        stats = collection['stats']

        stats = OpenseaCollection(
            collection_slug = collection['slug'],
            created_date    = collection['created_date'],
            market_cap      = stats['market_cap'],
            num_owners      = stats['num_owners'],
            floor_price     = stats['floor_price'],
            total_volume    = stats['total_volume'],
            total_sales     = stats['total_sales'],
            total_supply    = stats['total_supply'],
            thirty_day_volume = stats['thirty_day_volume'],
            thirty_day_change = stats['thirty_day_change'],
            thirty_day_sales  = stats['thirty_day_sales'],
            thirty_day_average_price = stats['thirty_day_average_price']
        )

        return stats      

    def fetch_collection(
        self, 
        collection_slug=None
    ):

        url = f'https://api.opensea.io/api/v1/collection/{collection_slug}'
        response_json = self._make_request(url)
        return response_json        

if __name__ == '__main__':

    collection_slug = 'mutant-ape-yacht-club'

    opensea_collection_stats = OpenseaCollectionStats()
    response_json = opensea_collection_stats.fetch_collection(collection_slug)
    stats = opensea_collection_stats.parse_collection(response_json)
    print (stats)