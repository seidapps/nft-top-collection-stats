import csv
from os import listdir
from os.path import isfile, join

from opensea_collection_stats import OpenseaCollectionStats
from utils import Utils

class OpenseaTopCollectionScraper:

    def __init__(self):
        
        self.utils = Utils()

    def opensea_collection_stats(self):

        # Get all collection slugs saved in files
        collection_slugs = []
        filenames = [f for f in listdir('data/') if isfile(join('data/', f))]
        for filename in filenames:

            with open('data/' + filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    collection_slugs.append(row[0])        

        # Get stats for collections
        collection_slug_stats = []
        opensea_collection_stats = OpenseaCollectionStats()
        for collection_slug in collection_slugs:

            print (f"Collection slug: {collection_slug}")

            try:
                response_json = opensea_collection_stats.fetch_collection_stats(collection_slug)
                stats = opensea_collection_stats.parse_collection_stats(response_json)
                collection_stats = [collection_slug] + list(stats.values())
                print (collection_stats)
                collection_slug_stats.append(collection_stats)
            except:
                continue

        # Save to CSV file
        self.utils.export_to_csv_file('data/top_collection_stats_2.csv', collection_slug_stats)
        
if __name__ == '__main__':

    opensea_top_collection_scraper = OpenseaTopCollectionScraper()
    opensea_top_collection_scraper.opensea_collection_stats()