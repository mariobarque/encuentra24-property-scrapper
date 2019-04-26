from bs4 import BeautifulSoup
import requests

province = 'provincia'
category_literal = 'categoria:'
price_literal = 'precio:'


class PropertyPageScrapper:

    def __init__(self, url):
        url = 'https://encuentra24.com' + url
        page = requests.get(url)
        self.soup = BeautifulSoup(page.text, 'html.parser')
        self.data = self.get_data()


    def get_data(self):
        data = dict()
        info_names = self.soup.find_all(class_='info-name')

        for info_name in info_names:
            info_value = info_name.find_next_sibling(class_='info-value')

            if info_value:
                data[info_name.get_text().strip().lower()] = info_value.get_text().strip().lower()

        return data


    def complete_property(self, prop):
        category = self.get_category()
        price = self.get_price()
        construction_size = self.get_construction_size()
        construction_year = self.get_construction_year()
        size = self.get_size()
        rooms = self.get_rooms()
        price_reduced = self.get_price_reduced()
        location = self.get_location()

        prop.complete(location, price, size, construction_size, construction_year, rooms, category, price_reduced)
        
        return prop


    def get_property_item(self, property_name):
        if property_name in self.data:
            return self.data[property_name]

        return None


    def get_category(self):
        return self.get_property_item(category_literal)


    def get_price(self):
        price = self.get_property_item(price_literal)
        if price:
            return price.split(".")[0].replace(',', '')
        return 0


    def get_construction_size(self):
        if 'm²' in self.data:
            return self.data['m²']

        if 'm² de construcción:' in self.data:
            return self.data['m² de construcción:']

        return None

    def get_construction_year(self):
        if 'año de construcción:' in self.data:
            return self.data['año de construcción:']

        return None


    def get_size(self):
        if 'tamaño del lote:' in self.data:
            return self.data['tamaño del lote:']

        if 'tamaño del lote m²:' in self.data:
            return self.data['tamaño del lote m²:']

        return self.get_construction_size()


    def get_rooms(self):
        if 'recámaras:' in self.data:
            return self.data['recámaras:']

        return None


    def get_price_reduced(self):
        price_reduced = self.soup.find(class_='ann-price-reduced')
        if price_reduced:                                 # remove the )
            return price_reduced.get_text().split(' ')[-1][:-1]


    def get_location(self):
        breadcrumb = self.soup.find(class_='breadcrumb')

        if breadcrumb is None:
            return ''

        elements = breadcrumb.find_all('a')
        found_province = False
        location = ''
        for element in elements:
            if province in element.get_text():
                found_province = True

            if found_province:
                location += element.get_text().strip() + ' | '

        return location[: -3]