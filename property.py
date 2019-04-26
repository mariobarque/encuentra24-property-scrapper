

class Property:
    def __init__(self, title, time_in_market, url):
        self.title = title
        self.time_in_market = time_in_market
        self.url = url

        # load defaults
        self.location = ''
        self.price = 0
        self.size = 0
        self.construction_size = 0
        self.construction_year = 0
        self.rooms = 0
        self.category = ''
        self.price_reduced = '0%'


    def complete(self, location, price, size, construction_size, construction_year, rooms, category, price_reduced):
        self.location = location
        self.price = price
        self.size = size
        self.construction_size = construction_size
        self.construction_year = construction_year
        self.rooms = rooms
        self.category = category
        self.price_reduced = price_reduced
