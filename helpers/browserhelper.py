from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


class BrowserHelper:

    @staticmethod
    def get_soup(page_url, class_that_should_be_loaded='ann-box-title'):

        # Getting error: selenium.common.exceptions.WebDriverException: Message: unknown error: unable to discover open pages
        try:
            browser = BrowserHelper.get_browser()
            browser.get(page_url)
        except:
            return None

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

    @staticmethod
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