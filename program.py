
from csv import writer
import multiprocessing as mp

import sys

import time

from paginationhelper import PaginationHelper
from propertypostprocessor import PropertyPostProcessor


def main():
    pages = PaginationHelper.get_pages()
    print('Total pages: %d' % pages)

    page_array = [(page,) for page in range(1, pages+1)]

    pool = mp.Pool(8)
    pool.starmap(get_and_save_page, page_array)


def get_and_save_page(page):
    properties = PropertyPostProcessor.process_post(page)
    with open('data/properties_%d.csv' % page, 'w', encoding='utf-8-sig') as csv_file:
        csv_writer = writer(csv_file)
        headers = ['Title', 'Location', 'Price', 'Time in Market', 'Size', 'Rooms', 'URL']
        csv_writer.writerow(headers)

        for p in properties:
            csv_writer.writerow([p.title, p.location, p.price,
                                 p.time_in_market, p.size, p.rooms, p.url])

    print('Done Processing page: ' + str(page) + ', with ' + str(len(properties)) + ' properties')

main()