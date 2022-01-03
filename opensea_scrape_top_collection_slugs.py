import csv
from os import listdir
from os.path import isfile, join

from dataclasses import asdict
from opensea_collection_stats import OpenseaCollection, OpenseaCollectionStats
from utils import Utils

class OpenseaTopCollectionScraper:

    def __init__(self):
        
        self.utils = Utils()        

    def get_collection_slugs_saved(self):

        collection_slugs_saved = []

        try:
            with open('data/top_collection_stats.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    collection_slugs_saved.append(row[0])    
        except:
            pass
        
        return collection_slugs_saved

    def opensea_collection_stats(self):

        # Get all collection slugs saved in files
        collection_slugs = []
        filenames = [f for f in listdir('data/') if isfile(join('data/', f))]
        for filename in filenames:

            with open('data/' + filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    collection_slugs.append(row[0])   

        # Get collection slugs with already saved stats
        collection_slugs_saved = self.get_collection_slugs_saved()
        print (f"Collections saved: {len(collection_slugs_saved)}")

        # Get stats for collections
        # Exclude collections already saved
        collection_slug_stats = []
        opensea_collection_stats = OpenseaCollectionStats()
        for collection_slug in collection_slugs:

            if collection_slug not in collection_slugs_saved:

                print (f"Collection slug: {collection_slug}")

                try:
                    response_json = opensea_collection_stats.fetch_collection(collection_slug)
                    collection_stats = opensea_collection_stats.parse_collection(response_json)
                    collection_slug_stats.append(asdict(collection_stats).values())                
                except:
                    continue

        # Save to CSV file
        if len(collection_slugs_saved) == 0:
            header = list(OpenseaCollection.__annotations__.keys())
        else:
            header = None

        self.utils.export_to_csv_file(
            filename='data/top_collection_stats.csv', 
            header=header, 
            rows=collection_slug_stats
        )
        
if __name__ == '__main__':

    opensea_top_collection_scraper = OpenseaTopCollectionScraper()
    opensea_top_collection_scraper.opensea_collection_stats()