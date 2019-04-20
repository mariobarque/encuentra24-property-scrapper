from bs4 import BeautifulSoup
import requests


class PropertyPageScrapper:

    @staticmethod
    def get_location(url):
        url = 'https://encuentra24.com' + url
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        breadcrumb = soup.find(class_='breadcrumb')
        elements = breadcrumb.find_all('a')
        found_province = False
        location = ''
        for element in elements:
            if 'provincia' in element.get_text():
                found_province = True

            if found_province:
                location += element.get_text().strip() + ' | '

        return location[: -3]