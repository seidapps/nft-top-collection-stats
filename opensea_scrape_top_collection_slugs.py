import csv
from os import listdir
from os.path import isfile, join

from opensea_collection_stats import OpenseaCollectionStats

def opensea_collection_stats():

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

        try:
            response_json = opensea_collection_stats.fetch_collection_stats(collection_slug)
            stats = opensea_collection_stats.parse_collection_stats(response_json)
            print (collection_slug, stats)
            collection_slug_stats.append([collection_slug] + stats.values())
        except:
            raise ValueError(f"Not able to query collection slug: {collection_slug}")

if __name__ == '__main__':

    # response = OpenseaCollectionStats().opensea_collection_stats('mutant-ape-yacht-club')
    # print (response)

    opensea_collection_stats()