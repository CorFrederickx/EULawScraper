"""scraping documents from the found search results pages"""

from abc import ABC, abstractmethod

import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from bs4 import BeautifulSoup
from urllib.parse import urlparse

from collections import OrderedDict

class BaseScraper(ABC):

    """Abstract base class for scraping found legislation"""

    logger = logging.getLogger(__name__)

    @abstractmethod
    def uses_driver(self):
        pass


    @abstractmethod
    def create_driver(self):
        pass


    @abstractmethod
    def has_pagination(self):
        pass


    @abstractmethod
    def get_pagination_urls(self):
        pass


    @abstractmethod
    def scrape_documents(self):
        pass


    def __init__(self, base_url: str):

        """
        Initialize an instance of the scraper with a base_url

        :param base_url: The URL of the search results page that was build by the BaseSearchURL class.
        """

        parsed = urlparse(base_url)
        if not (parsed.scheme and parsed.netloc):
            raise ValueError(f"Invalid URL: {base_url}")
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}

        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retries))
        self.session.mount("http://", HTTPAdapter(max_retries=retries))
        self.session.headers.update(self.headers)

        
    def fetch_response(self, url):

        """
        Fetches and returns the HTTP response object for a given URL. If the request fails, it returns None
        """

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None
        

    def fetch_pdf_response(self, url):

        """
        If the HTTP response object of given URL is valid, the content of the response is returned, or None on failure.
        Used in europarl_scraper.py, where content consists of text in a PDF.
        """

        response = self.fetch_response(url)
        if not response:
            return None
        return response.content
    

    def get_soup(self, url):

        """
        Turns the HTTP response object of given URL into a BeautifulSoup object for parsing HTML content. 
        Returns None on failure. 
        """

        response = self.fetch_response(url)
        if response:
            return BeautifulSoup(response.text, 'html.parser')
        return None
    

    def download_file(self, url, filename):

        """
        Downloads a file from given URL and saves it locally under given filename.
        If successful, a confirmation is logged. Any error occuring is catched as an exception and also logged.
        Used in european_commission_scraper.py only.
        """

        response = self.fetch_response(url)
        if not response:
            self.logger.error(f"No response for {url}, skipping download.")
            return
        try:
            with open(filename, "wb") as f:
                f.write(response.content)
            self.logger.info(f"Downloaded: {filename}")
        except OSError as e:
            self.logger.error(f"Failed to write file {filename}: {e}")


    def __call__(self):

        """
        Executes the scraping process.

        Initializes a webdriver, collects URLs from paginated pages and URLs of all documents on those pages and associated metadata. 
        The documents are then scraped.

        Whether a step in this process is necessary is defined by sub-class functions found in all scraper classes:
            - uses_driver()
            - has_pagination()
            - extracts_metadata()

        """

        driver = self.create_driver() if self.uses_driver() else None

        try:
            pages = self.get_pagination_urls(driver if self.uses_driver() else None) if self.has_pagination() else [self.base_url]
            self.logger.info(f"Total pages: {len(pages)}")

            all_urls = self.collect_all_document_urls(pages, driver)
            self.logger.info(f"Total downloadable documents found: {len(all_urls)}")

            self.logger.info("Start scraping")
            self.scrape_documents(all_urls)

        finally:
            if driver:
                driver.quit()


    def collect_all_document_urls(self, pages, driver=None):
        
        """
        Helper function for '__call__': iterates over each page URL, collects document URLs from each page and finally returns a list of unique document URLs
        Optionally metadata is extracted, depending on the extracts_metadata() function in the associated subclass.
        """

        unique = OrderedDict() # leaving out duplicates, while keeping natural discovery order

        for page_url in pages:
            self.logger.info(f"Processing page: {page_url}")

            doc_urls = self.collect_document_urls(page_url, driver)
            self.logger.info(f"Document URLs: {doc_urls}")

            if self.extracts_metadata():
                self.extract_metadata(page_url, driver)

            for url in doc_urls:
                unique.setdefault(url, None)
            
        return list(unique.keys())




        

