import time
import requests
import os

from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

@dataclass
class OpenseaCollectionStats:
    token_id: int
    name: str
    image_url: str
    open_sea_link: str
    collection_slug: str
    floor_price: float = None

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
            print ("Sleeping 5 seconds and trying again...")
            time.sleep(5)            
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

    def parse_collection_stats(self, response_json):

        # {
        #   "stats": {
        #     "one_day_volume": 6552.161685668852,
        #     "one_day_change": -0.021646283395056823,
        #     "one_day_sales": 356.0,
        #     "one_day_average_price": 18.404948555249586,
        #     "seven_day_volume": 24094.95526632172,
        #     "seven_day_change": 0.5407546528453521,
        #     "seven_day_sales": 1588.0,
        #     "seven_day_average_price": 15.173145633703852,
        #     "thirty_day_volume": 46625.94611710244,
        #     "thirty_day_change": 0.5839917242074927,
        #     "thirty_day_sales": 3981.0,
        #     "thirty_day_average_price": 11.71211909497675,
        #     "total_volume": 169821.10301226383,
        #     "total_sales": 22183.0,
        #     "total_supply": 17635.0,
        #     "count": 17635.0,
        #     "num_owners": 11166,
        #     "average_price": 7.6554615251437514,
        #     "num_reports": 17,
        #     "market_cap": 267578.42325036746,
        #     "floor_price": 16.1
        #   }
        # }

        return response_json['stats']        

    def fetch_collection_stats(
        self, 
        collection_slug=None
    ):

        url = f'https://api.opensea.io/api/v1/collection/{collection_slug}/stats/'
        response_json = self._make_request(url)
        return response_json

if __name__ == '__main__':

    collection_slug = 'mutant-ape-yacht-club'

    opensea_collection_stats = OpenseaCollectionStats()
    response_json = opensea_collection_stats.fetch_collection_stats(collection_slug)
    stats = opensea_collection_stats.parse_collection_stats(response_json)
    print (stats)