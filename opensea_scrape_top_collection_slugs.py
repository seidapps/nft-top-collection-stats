import csv
from os import listdir
from os.path import isfile, join, exists

from dataclasses import asdict
from opensea_collection_stats import OpenseaCollection, OpenseaCollectionStats
from utils import Utils

class OpenseaTopCollectionScraper:

    def __init__(self):
        
        self.utils = Utils()  

    def get_collection_slugs(self):
        """
        Function iterates through the filenames - represented in page form - saved in the data folder that
        contain CoinGecko collection slugs. 
        Check if the CoinGecko slug has a different OpenSea slug from the manually created
        dictionary.
        If is, update to Opensea slug.
        """

        collection_slug_list = []
        filename = 'data/coingecko_opensea_mapping.json'
        slug_mapping_dict = self.utils.import_json_file(filename)   

        # Get collection slugs from file - update to opensea name if necessary
        filenames = [f for f in listdir('data/') if isfile(join('data/', f))]
        for filename in filenames:

            if 'page_' in filename:

                with open('data/' + filename, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        collection_slug = row[0]
                        if collection_slug in slug_mapping_dict.keys():
                            value = slug_mapping_dict[collection_slug]
                            if value != "":
                                collection_slug = value
                        
                        collection_slug_list.append(collection_slug)               

        return collection_slug_list

    def get_collection_slugs_saved(self):
        """
        Determine whether the top collection stats file exists.
        If it does exist, extract all saved slugs to avoid duplicates. 
        If not, create file with header column names equal to the OpenseaCollection collection dataclass.
        """

        collection_slugs_saved = []

        filename = 'data/top_collection_stats.csv'
        file_exists = exists(filename)

        if file_exists:

            with open(filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    collection_slugs_saved.append(row[0])                
        else:
            with open(filename, 'a') as f:
                write = csv.writer(f)     
                write.writerow(list(OpenseaCollection.__annotations__.keys()))
        
        return collection_slugs_saved

    def opensea_collection_stats(self):
        """
        Main function to extract collection stats.

        Function will pull the collection slugs names, collection stats on each collection,
        and save to CSV file. 

        If collection does not exist. The collection slug will be added to an invalid collection stats CSV.
        """

        # Get collection slugs
        collection_slug_list = self.get_collection_slugs()

        # Get collection slugs with already saved stats
        collection_slugs_saved = self.get_collection_slugs_saved()
        print (f"Collections saved: {len(collection_slugs_saved)}")

        # Get stats for collections
        # Exclude collections already saved
        opensea_collection_stats = OpenseaCollectionStats()
        for collection_slug in collection_slug_list:

            if collection_slug not in collection_slugs_saved:

                print (f"Collection slug: {collection_slug}")

                try:
                    response_json = opensea_collection_stats.fetch_collection(collection_slug)
                    collection_stats = opensea_collection_stats.parse_collection(response_json)
                    self.utils.export_to_csv_file(
                        filename='data/top_collection_stats.csv', 
                        rows=[asdict(collection_stats).values()]
                    )               
                except:
                    self.utils.export_to_csv_file(
                        filename='data/invalid_collection_slugs.csv', 
                        rows=[[collection_slug]]
                    ) 
        
if __name__ == '__main__':

    opensea_top_collection_scraper = OpenseaTopCollectionScraper()
    opensea_top_collection_scraper.opensea_collection_stats()