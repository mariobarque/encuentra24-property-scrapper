
from csv import writer
import multiprocessing as mp

import sys
import os
import glob
import pandas as pd


from paginationhelper import PaginationHelper
from propertypostprocessor import PropertyPostProcessor


def main():
    #scrap_data()
    merge_csv_files()

def scrap_data():
    pages = PaginationHelper.get_pages()

    print('Total pages: %d' % pages)
    page_array = [(page,) for page in range(1, pages+1)]

    #page_array = [(page,) for page in  [4, 58, 48, 90, 84, 434, 83, 100, 3, 435, 91, 128, 436, 46, 60, 92, 1, 47, 59, 2, 89, 82, 433]]

    pool = mp.Pool(10)
    pool.starmap(get_and_save_page, page_array)

    print('Done scrapping data.')


def merge_csv_files():
    os.chdir(os.getcwd() + "/data")
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    df = pd.concat([pd.read_csv(f) for f in all_filenames])
    df = df.dropna(axis=0, how='any')

    df.to_csv("properties.csv", index=False, encoding='utf-8-sig')

    print('Done merging.')

def get_and_save_page(page):
    properties = PropertyPostProcessor.process_post(page)
    print('Done processing page: %d with %d properties' % (page, len(properties)))

    headers = ['Title', 'Location', 'Price', 'Time in Market', 'Size', 'Rooms', 'URL']
    csv_content = []
    for p in properties:
        # Unexpected typeerror happened
        csv_content.append(['' if hasattr(p, 'title') == False else p.title,
                            '' if hasattr(p, 'location') == False else p.location,
                            '' if hasattr(p, 'price') == False else p.price,
                            '' if hasattr(p, 'time_in_market') == False else p.time_in_market,
                            '' if hasattr(p, 'size') == False else p.size,
                            '' if hasattr(p, 'rooms') == False else p.rooms,
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