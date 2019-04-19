import sys
from bs4 import BeautifulSoup
from property import Property
from csv import writer
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


base_path = 'https://www.encuentra24.com/costa-rica-es/searchresult/bienes-raices-venta-de-propiedades#search=f_currency.usd|number.50&page='
properties = []

def is_property_valid(title, location, price):
    if title and location and price:
        return True

    print('Invalid Property: '+ title + ' | ' + price + ' | ' + location)
    return False


def get_time_in_market(post):
    segment = post.find(class_='ann-box-hilight-time')
    if segment is None:
        return 'N/A'

    time_in_market = segment.find(class_='value').get_text()
    return time_in_market.strip()


def get_size_and_rooms(post):
    segment = post.find_all(class_='hide-on-hover-1024')
    size = segment[0].find(class_='value').get_text().split(" ")[0]
    rooms = 0
    if len(segment) == 2:
        rooms = segment[1].find(class_='value').get_text()

    return size, rooms


def get_title(post):
    segment = post.find(class_='ann-box-details').find_all('strong')
    if len(segment) > 0:
        return segment[0].get_text().strip()
    else:
        return post.find(class_='ann-box-details').find_all('span')[0].get_text().strip()


def get_price(post):
    price = post.find(class_='ann-price').get_text().split(" ")[0]
    return price.replace(',','')


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

    return location


def process_page(page):
    url = base_path + str(page)
    print(url)
    soup = get_soup(url)
    if soup is None:
        return

    posts = soup.find_all('article')

    for post in posts:
        title = get_title(post)
        url = post.find(class_='ann-box-title')['href']
        #location = post.find(class_='ann-info-item').get_text().strip()
        location = get_location(url)
        price = get_price(post)
        size, rooms = get_size_and_rooms(post)
        time_in_market = get_time_in_market(post)

        if is_property_valid(title,location,price):
            properties.append(Property(title, location, price, time_in_market, size, rooms, url))


def get_soup(page_url, class_that_should_be_loaded = 'ann-box-title'):
    browser = get_browser()
    browser.get(page_url)

    try:
        WebDriverWait(browser, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, class_that_should_be_loaded)))
        html = browser.page_source
    except TimeoutException:
        return None
    finally:
        browser.quit()

    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_browser():
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')  # # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(30)

    return browser


def get_pages():
    soup = get_soup(base_path + '1')
    if soup is None:
        sys.exit()

    listing_numbers = soup.find(class_='listing-numbers').get_text().strip()
    if listing_numbers is not None:
        split = listing_numbers.split(' ')
        if len(split) > 1:
            total_posts = int(split[1])
            return int(total_posts/50)

    return 1


def main():
    pages = get_pages()

    with open('properties.csv', 'w', encoding='utf-8-sig') as csv_file:
        csv_writer = writer(csv_file)
        headers = ['Title', 'Location', 'Price', 'Time in Market', 'Size', 'Rooms', 'URL']
        csv_writer.writerow(headers)

        for page in range(171, pages + 1):
            print('Starting Processing page: ' + str(page))
            properties.clear()
            process_page(page)
            print('Done Processing page: ' + str(page) + ', with ' + str(len(properties)) + ' properties')
            for p in properties:
                csv_writer.writerow([p.title, p.location, p.price,
                                     p.time_in_market, p.size, p.rooms, p.url])


main()