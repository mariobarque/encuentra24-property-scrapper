
from csv import writer
import multiprocessing as mp

import sys
import os
import glob
import pandas as pd

from database.database import Database
from helpers.paginationhelper import PaginationHelper
from propertypostprocessor import PropertyPostProcessor


max_retries = 5
existing_urls = Database.get_urls()

def main():
    scrap_data()
    merge_csv_files()

def scrap_data():
    pages = PaginationHelper.get_pages()

    print('Total pages: %d' % pages)
    page_array = [(page,) for page in range(1, pages+1)]

    retries = 0

    while retries < max_retries:
        try:
            pool = mp.Pool(32)
            pool.starmap(get_and_save_page, page_array)

            print('Done scrapping data.')
            break
        except:
            print(sys.exc_info()[0])
            files = os.listdir("data")
            processed_numbers = []
            all_numbers = [i for i in range(1, pages)]
            for file in files:
                if file.endswith('.csv'):
                    processed_numbers.append(int(file.replace('properties_', '').replace('.csv', '')))

            missing = set(all_numbers) - set(processed_numbers)
            print('Missing:')
            print(missing)

            page_array = missing
            retries += 1
            print('Retrying...')


def merge_csv_files():
    os.chdir(os.getcwd() + "/data")
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    df = pd.concat([pd.read_csv(f) for f in all_filenames])
    df = df.dropna(axis=0, subset=['Location', 'Price'])

    df.to_csv("properties.csv", index=False, encoding='utf-8-sig')

    print('Done merging.')


def get_and_save_page(page):
    properties = PropertyPostProcessor.process_post(page)
    if properties is None:
        print('Error with page number %d' % page)
        raise Exception('Error processing a page...')

    print('Done processing page: %d with %d properties' % (page, len(properties)))
    save_page(properties, page)


def save_page(properties, page):
    headers = ['Title', 'Location', 'Price', 'Time in Market', 'Size', 'Construction Size',
               'Construction Year', 'Rooms', 'Category', 'Price Reduced', 'URL']
    csv_content = []
    for p in properties:
        # Unexpected typeerror happened
        csv_content.append(['' if hasattr(p, 'title') == False else p.title,
                            '' if hasattr(p, 'location') == False else p.location,
                            '' if hasattr(p, 'price') == False else p.price,
                            '' if hasattr(p, 'time_in_market') == False else p.time_in_market,
                            '' if hasattr(p, 'size') == False else p.size,
                            '' if hasattr(p, 'construction_size') == False else p.construction_size,
                            '' if hasattr(p, 'construction_year') == False else p.construction_year,
                            '' if hasattr(p, 'rooms') == False else p.rooms,
                            '' if hasattr(p, 'category') == False else p.category,
                            '' if hasattr(p, 'price_reduced') == False else p.price_reduced,
                            '' if hasattr(p, 'url') == False else p.url])

    with open('data/properties_%d.csv' % page, 'w', encoding='utf-8-sig') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(headers)

        tries = 0

        while tries < 3:
            try:
                csv_writer.writerows(csv_content)
                break
            except:
                print("Unexpected error: %s" % sys.exc_info()[0])
                tries += 1



main()