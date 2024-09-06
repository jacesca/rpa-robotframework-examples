import re

from resources.types import ParameterProcess
from resources.locations import (NEWS_URL, LOCAL_EXCEL_FILE,
                                 LOCAL_IMAGE_NEWS, LOCAL_IMAGE_FOLDER,
                                 LOCAL_ZIP_FILE)
from resources.locators import (SEARCH_BUTTON,
                                SEARCH_INPUT_TEXT,
                                DROPDOWN_SEARCH_ORDER,
                                DROPDOWN_SEARCH_LABEL_ORDER,
                                COOKIES_REQUEST_BUTTON,
                                MORE_NEWS_BUTTON,
                                RESULT_CONTAINER)

from time import sleep
from datetime import datetime, timedelta
from robocorp import storage, log, workitems
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select, WebDriverWait
from RPA.HTTP import HTTP
from RPA.Archive import Archive
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from bs4 import BeautifulSoup


class ProcessConfiguration:
    """
    Class to handle the parameters for RPA Collect News execution
    """

    def __init__(self) -> None:
        """Initialize the Parameter class"""
        self.params = {}

    def get_parameters_from_cloud_storage(self) -> ParameterProcess:
        """Get the process parameters"""
        assets = storage.get_json('RPA Collect News Assets')
        parameters = {
            'search_key': assets['search_key'],
            'month_range': assets['month_range']
        }
        log.info('Parameters were read from Robocorp Cloud!')
        self.params = parameters

    def save_parameters_to_workitems(self) -> None:
        """Save the process parameters to work item"""
        workitems.outputs.create(self.params)
        pass


class NewsScrapper:
    """
    Class to handle web scraping of news from the News WebSite
    """

    def __init__(self) -> None:
        """Initialize the NewsScrapper with the browser instance"""
        self.browser = Selenium()
        self.url = NEWS_URL
        self.timeout = 10
        self.params = None
        self.search_key = None
        self.month_range = None
        self.header = None
        self.html = None
        log.info('NewsScrapper object initialized!')

    def _scroll_page(self) -> None:
        """Scroll page to mimic human interaction"""
        self.browser.execute_javascript(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def _wait_until_page_is_loaded(self) -> None:
        """Implicit Wait until page is loaded"""
        WebDriverWait(self.browser.driver, self.timeout).until(
            lambda driver: driver.execute_script(
                "return document.readyState"
            ) == "complete"
        )

    def _is_element_in_page(self, locator: str) -> bool:
        try:
            self.browser.wait_until_page_contains_element(
                locator, self.timeout
            )
            return True
        except Exception as e:
            log.warn(f'{locator}: {e}')
            return False

    def start_environment(self) -> None:
        """Prepare environment and load parameters to run automation."""
        # Load parameters
        workkitem = workitems.inputs.current
        params = workkitem.payload

        # Save the parametrization
        self.search_key = params['search_key']
        self.month_range = params['month_range']
        log.info(f'Loaded parameters: {params}')

    def open_website(self) -> None:
        """Open the browser and navigate to the News website."""
        try:
            self.browser.open_available_browser(self.url)
            self.browser.wait_until_page_contains_element(
                COOKIES_REQUEST_BUTTON, self.timeout
            )
            self._scroll_page()
            self.browser.click_element(COOKIES_REQUEST_BUTTON)
        except WebDriverException as e:
            log.info(f'Failed to open browser: {e}')

    def filter_by_search_key(self) -> None:
        """Locate search button and add search key to filter visible news."""
        self.browser.click_element(SEARCH_BUTTON)
        self.browser.input_text(SEARCH_INPUT_TEXT, self.search_key)
        self.browser.press_keys(SEARCH_INPUT_TEXT, "ENTER")

    def order_by_date(self) -> None:
        """Order the result by date"""
        self.browser.wait_until_page_contains_element(
            DROPDOWN_SEARCH_ORDER, self.timeout
        )
        dropdown = Select(self.browser.find_element(DROPDOWN_SEARCH_ORDER))
        dropdown.select_by_visible_text(DROPDOWN_SEARCH_LABEL_ORDER)

    def getting_more_news_if_available(self) -> None:
        """ClicK on more news button if it exists"""
        self._wait_until_page_is_loaded()
        while self._is_element_in_page(MORE_NEWS_BUTTON):
            element = self.browser.find_element(MORE_NEWS_BUTTON)
            self.browser.driver.execute_script(
                "arguments[0].click();", element
            )

    def extract_html_result(self) -> None:
        """Extract html of content news"""
        if self._is_element_in_page(RESULT_CONTAINER):
            self.html = self.browser.get_element_attribute(
                RESULT_CONTAINER, 'outerHTML'
            )
            log.info('HTML extracted:')
            log.info(self.html)
        else:
            log.info('No data found!')

    def clean_html_result(self) -> None:
        """Rid off innecesary html elements"""
        if self.html:
            soup = BeautifulSoup(self.html, 'html.parser')

            # Extract articles
            articles = soup.find_all('article')
            self.header = ['id', 'title', 'date_descrip', 'news_url',
                           'image_src']
            html = []
            for index, item in enumerate(articles):
                title = item.find('h3').get_text(strip=True)
                date_descrip = item.find(
                    'div', class_='gc__excerpt'
                ).get_text(strip=True)
                image_src = item.find('img')['src']
                news_url = item.find('a')['href']
                html.append((index, title, date_descrip, news_url, image_src))

            self.html = html
            log.info('html:')
            log.info(self.header)
            log.info(self.html)

    def save_html_to_workitems(self) -> None:
        """Save extracted html to work item"""
        payload = {
            'search_key': self.search_key,
            'month_range': self.month_range,
            'header': self.header,
            'html': self.html
        }
        workitems.outputs.create(payload)


class NewsDataTable:
    """
    Class to handle data format and export to excel
    """
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the NewsDataTable with the data extracted"""
        # Load html extracted
        workkitem = workitems.inputs.current
        self.html = workkitem.payload['html']
        self.search_key = workkitem.payload['search_key']
        self.month_range = workkitem.payload['month_range']
        self.header = workkitem.payload['header']
        date_init = {'day': 1,
                     'hour': 0, 'minute': 0, 'second': 0, 'microsecond': 0}
        if self.month_range in [0, 1]:
            self.date_threshold = datetime.now().replace(**date_init)
        else:
            new_date = datetime.now() - timedelta(days=31)
            self.date_threshold = new_date.replace(**date_init)
        self.table = [('id', 'title', 'date', 'description', 'image',
                       'key coincidence count', 'money detected',
                       'news_url', 'img_url')]
        self.images = []

    def format_table(self) -> None:
        """Parse html to extract news data and images url"""
        if self.html:
            for item in self.html:
                item = {self.header[i]: item[i] for i in range(len(item))}

                index = item['id']
                title = item['title']

                date_descrip = item['date_descrip'].split('...')
                date_descrip = list(map(str.strip, date_descrip))  # No spaces
                date_descrip = list(filter(None, date_descrip))  # No empty
                date = date_descrip[0]
                if ('hour' in date) or ('minute' in date):
                    date = datetime.now()
                elif 'day' in date:
                    days = int(date.split(' ')[0])
                    date = datetime.now() - timedelta(days=days)
                else:
                    date = datetime.strptime(date, '%b %d, %Y')
                description = date_descrip[1]

                image_src = item['image_src']
                if 'https://' in image_src:
                    image_filename = LOCAL_IMAGE_NEWS.format(index).split('/')[-1]  # noqa
                else:
                    image_src = ''
                    image_filename = ''
                news_url = item['news_url']

                key_count = (title.count(self.search_key) +
                             description.count(self.search_key))

                money_regex = r"(\$\s?\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+(?:\.\d{1,2})?\s?(?:USD|dollars))"  # noqa
                money = re.search(money_regex, description + title)
                money = 'True' if money else 'False'

                if date >= self.date_threshold:
                    date = date.strftime('%Y/%m/%d')
                    self.table.append((index, title, date, description,
                                       image_filename, key_count, money,
                                       news_url, image_src))
                    self.images.append((index, image_src))
                else:
                    break

            log.info(f'date_threshold: {self.date_threshold}')
            log.info('Parsed Html:')
            log.info(self.table)
            log.info('Images found')
            log.info(self.images)
        else:
            log.info('No data found!')

    def export_as_excel_file(self) -> None:
        """Saving parsed html as table"""
        excel = Files()
        excel.create_workbook(LOCAL_EXCEL_FILE)
        excel.append_rows_to_worksheet(self.table)
        excel.save_workbook()

    def save_images_to_workitems(self) -> None:
        """Saving images url to workitems"""
        workitems.outputs.create({'images': self.images})


class ImageRegistor:
    """
    Class to download the image news
    """
    def __init__(self, *args, **kwargs) -> None:
        """Initialize the ImageRegistor with the image details"""
        # Load html extracted
        workkitem = workitems.inputs.current
        self.images = workkitem.payload['images']

    def download_images(self) -> None:
        """Download the News images"""
        http = HTTP()
        for index, img_url in self.images:
            if img_url:
                filename = LOCAL_IMAGE_NEWS.format(index)
                http.download(
                    url=img_url,
                    target_file=filename,
                    overwrite=True
                )
                sleep(2)

    def archive_images(self) -> None:
        """Create a ZIP file of news images files."""
        lib = Archive()
        lib.archive_folder_with_zip(LOCAL_IMAGE_FOLDER, LOCAL_ZIP_FILE)
