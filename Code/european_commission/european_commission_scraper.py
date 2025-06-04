import logging
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

from scraper import BaseScraper

class EuropeanCommissionScraper(BaseScraper):

    logger = logging.getLogger(__name__)

    """
    Class for scraping documents from the European Commission website, extending BaseScraper.
    """

    def uses_driver(self):

        """
        Indicates whether a WebDriver is required for scraping.
        The European Commission site does not require a WebDriver.
        """

        return False
    
    def create_driver(self):

        """
        Returns None since this scraper does not require a WebDriver.
        """

        return None

    def has_pagination(self):

        """
        Indicates whether the search results are paginated.
        Pagination is present.
        """

        return True

    def extracts_metadata(self):

        """
        Indicates whether metadata extraction is supported.
        This is not the case on the European Commission website.
        """

        return False

    def __init__(self, base_url):

        """
        Initializes a EuropeanCommissionScraper instance.

        :param base_url: The base URL of the European Commission search results page.
        """

        super().__init__(base_url)
        self.base_url = base_url
        
    def get_pagination_urls(self, driver=None):
         
        """
        Retrieves all paginated URLs from the search results page and returns them as a list.
        Returns only the base URL if no other pages are found.
        """

        paginated_urls = [self.base_url]
        soup = self.get_soup(self.base_url)

        if not soup:
            return paginated_urls

        last_page_item = soup.find('li', class_='ecl-pager__item--last')

        if not last_page_item:
            return paginated_urls # return base_url if there is no last page element

        last_page_link = last_page_item.find('a')

        if last_page_link:
            last_page_number = int(last_page_link['value'])
            paginated_urls.extend(self.base_url.replace('&page=', f'&page={page}')for page in range(2, last_page_number + 1))

        else:
            paginated_urls.append(self.base_url.replace('&page=', '&page=2'))

        self.logger.info(paginated_urls)
        return paginated_urls

    
    def collect_document_urls(self, url, driver=None):

        """
        Collects downloadable document URLs from a given search results page.

        :param url: The URL of the page to scrape.
        :return: List of unique document download URLs.
        """

        soup = self.get_soup(url)
        if not soup:
            return []
        
        unique_urls = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "document/download/" in href:
                full_url = urljoin(url, href)
                unique_urls.add(full_url)
            
        return list(unique_urls)
    
    def extract_filename_from_url(self, url):

        """
        Extracts ans returns the 'filename' parameter from a given document URL.
        Returns None if no such element is found.
        """

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("filename", [None])[0]

    def scrape_documents(self, document_urls):
        
        """
        Downloads and saves documents from the provided URLs using extracted filenames.

        :param document_urls: List of document download URLs.
        """
        
        for url in document_urls:
            filename = self.extract_filename_from_url(url)
            if not filename:
                self.logger.info(f"Filename not found in URL: {url}")
                continue
            self.download_file(url, filename)

