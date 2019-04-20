from browserhelper import BrowserHelper
from constants import Constants

from postscrapper import PostScrapper
from property import Property
from propertypagescrapper import PropertyPageScrapper


class PropertyPostProcessor:


    @staticmethod
    def process_post(page):

        url = Constants.base_path + str(page)
        print(url)
        soup = BrowserHelper.get_soup(url)
        if soup is None:
            return

        posts = soup.find_all('article')
        properties = []
        for post in posts:
            properties.append(PropertyPostProcessor.get_property(post))

        return properties


    @staticmethod
    def get_property(post):
        title = PostScrapper.get_title(post)
        url = post.find(class_='ann-box-title')['href']
        #location = post.find(class_='ann-info-item').get_text().strip()
        location = PropertyPageScrapper.get_location(url)
        price = PostScrapper.get_price(post)
        size, rooms = PostScrapper.get_size_and_rooms(post)
        time_in_market = PostScrapper.get_time_in_market(post)

        if PropertyPostProcessor.is_property_valid(title, location, price):
            return Property(title, location, price, time_in_market, size, rooms, url)

        return None


    @staticmethod
    def is_property_valid(title, location, price):
        if title and location and price:
            return True

        print('Invalid Property: '+ title + ' | ' + price + ' | ' + location)
        return False
