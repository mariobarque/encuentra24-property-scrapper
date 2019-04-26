from helpers.browserhelper import BrowserHelper
from constants import Constants

from scrappers.postscrapper import PostScrapper
from property import Property
from scrappers.propertypagescrapper import PropertyPageScrapper


class PropertyPostProcessor:


    @staticmethod
    def process_post(page, existing_urls):

        url = Constants.base_path + str(page)
        print(url)
        soup = BrowserHelper.get_soup(url)
        if soup is None:
            return

        posts = soup.find_all('article')
        properties = []
        for post in posts:
            properties.append(PropertyPostProcessor.get_property(post, existing_urls))

        return properties


    @staticmethod
    def get_property(post, existing_urls):
        title = PostScrapper.get_title(post)
        url = post.find(class_='ann-box-title')['href']
        time_in_market = PostScrapper.get_time_in_market(post)

        prop = Property(title, time_in_market, url)

        property_page_scrapper = PropertyPageScrapper(url)
        prop = property_page_scrapper.complete_property(prop)

        return prop


    @staticmethod
    def is_property_valid(title, location, price):
        if title and location and price:
            return True

        print('Invalid Property: '+ title + ' | ' + price + ' | ' + location)
        return False
