

class PostScrapper:

    @staticmethod
    def get_time_in_market(post):
        segment = post.find(class_='ann-box-hilight-time')
        if segment is None:
            return 'N/A'

        time_in_market = segment.find(class_='value').get_text()
        return time_in_market.strip()

    @staticmethod
    def get_size_and_rooms(post):
        segment = post.find_all(class_='hide-on-hover-1024')
        size = segment[0].find(class_='value').get_text().split(" ")[0]
        rooms = 0
        if len(segment) == 2:
            rooms = segment[1].find(class_='value').get_text()

        return size, rooms

    @staticmethod
    def get_title(post):
        segment = post.find(class_='ann-box-details').find_all('strong')
        if len(segment) > 0:
            return segment[0].get_text().strip()
        else:
            return post.find(class_='ann-box-details').find_all('span')[0].get_text().strip()

    def get_price(post):
        price = post.find(class_='ann-price').get_text().split(" ")[0]
        return price.replace(',', '')