import sys

from helpers.browserhelper import BrowserHelper
from constants import Constants


class PaginationHelper:

    @staticmethod
    def get_pages():
        soup = BrowserHelper.get_soup(Constants.base_path + '1')
        if soup is None:
            sys.exit()

        listing_numbers = soup.find(class_='listing-numbers').get_text().strip()
        if listing_numbers is not None:
            split = listing_numbers.split(' ')
            if len(split) > 1:
                total_posts = int(split[1])
                return int(total_posts / 50)

        return 1