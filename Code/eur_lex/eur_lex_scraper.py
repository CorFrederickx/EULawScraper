
import logging
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import json

from scraper import BaseScraper
from .standardize_metadata_eurlex import standardize_metadata
from metadata_schema import save_metadata_to_file

logger = logging.getLogger(__name__)

class EurLexScraper(BaseScraper):

    """
    Scraper class for extracting HTML documents and metadata from the EurLex website, extending BaseScraper.
    """

    def uses_driver(self):

        """
        Indicates whether a WebDriver is required for scraping. 
        EurLex does not require one.
        """

        return False
    
    def create_driver(self):

        """
        Returns None since this scraper does not require a WebDriver.
        """

        return None

    def has_pagination(self):

        """
        Indicates whether the EurLex results are paginated. 
        Pagination is present.
        """

        return True

    def extracts_metadata(self):

        """
        Indicates whether metadata can be extracted for each document. 
        EurLex supports metadata extraction.
        """
         
        return True

    def __init__(self, base_url):

        """
        Initializes an EurLexScraper instance with a base URL as input, and prepares metadata and document storage.
        
        :param base_url: The URL of the EurLex search results page as build in eur_lex_search.py.
        """

        super().__init__(base_url)
        
        self.metadata_list = [] # list of dictionaries containing the metadata, later saved as JSON with celex numbers as keys
        self.documents = []

    def get_pagination_urls(self, driver=None):

        """
        Retrieves all paginated URLs from the EurLex search results page and returns them as a list. 
        Returns only the base URL if no other pages are found.
        """

        paginated_urls = [self.base_url]
        soup = self.get_soup(self.base_url)

        if not soup:
            return paginated_urls # return at least the base URL

        last_page_link = soup.find('a', title='Last Page')

        if last_page_link:
            href = last_page_link['href']
            full_url = urljoin(self.base_url, href)
            last_page_number = parse_qs(urlparse(full_url).query).get('page', [1])[0]

            paginated_urls.extend(f"{self.base_url}&page={page}" for page in range(2, int(last_page_number) + 1))

        else:
            next_page_button = soup.find('span', class_='PaginationPage')
            if next_page_button:
                paginated_urls.append(f"{self.base_url}&page=2")

        return paginated_urls
    
    def parse_metadata_block(self, block):

        """
        Parses a metadata <dl> block into a dictionary of key-value pairs.
        
        :param block: a BeautifulSoup <dl> element containing metadata
        :return: a dictionary of extracted metadata
        """

        metadata = {}
        dt_elements = block.find_all('dt')
        dd_elements = block.find_all('dd')
        
        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.get_text(strip=True).replace(":", "")
            value = dd.get_text(strip=True)
            metadata[key] = value
        return metadata
    
    def extract_legal_status(self, div):

        """
        Determines whether a legal document is still in force based on its 'DocStatus' in the html.

        :param div: BeautifulSoup <div> element of a search result
        :return: a Boolean if legal status is found, otherwise None
        """

        status_div = div.find_previous('div', class_='DocStatus')
        if status_div:
            status_text = status_div.get_text(strip=True)
            return not "No longer in force" in status_text
        return None

    def build_celex_url(self, celex_number):

        """
        Constructs a full URL for a given CELEX number.
        """

        return f'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex_number}'
    
    # the opposite
    def extract_celex_number_from_url(self, url):

        """
        Extracts the CELEX number from a given document URL.
        Returns None if no 'uri' is found in the URLs parameters.
        """

        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if "uri" in query_params:
            return query_params["uri"][0].split(":")[-1]
        return None

    def build_metadata_dict(self):

        """
        Returns a metadata_list as a dictionary with CELEX numbers as keys.
        """

        return {
            item["CELEX number"]: item
            for item in self.metadata_list if "CELEX number" in item
        }
    
    def extract_metadata(self, url, driver=None):

        """
        Combines above functions to extract metadata from the EurLex search results page and standardize it.

        Saves the result to a local JSON file called 'metadata_eurlex.json'. 
        (see functions in the associated standardize_metadata_eurlex.py file and the metadata_schema.py)

        :param url: URL of the EurLex search results page
        """

        soup = self.get_soup(url)

        result_divs = soup.find_all('div', class_='SearchResultData collapse in')

        for div in result_divs:
            metadata = {}
            metadata_blocks = div.find_all('dl')

            for block in metadata_blocks:
                block_metadata = self.parse_metadata_block(block)
                metadata.update(block_metadata)

            in_force = self.extract_legal_status(div)
            if in_force is not None:
                metadata["In force"] = in_force

            if "CELEX number" in metadata:
                metadata["url"] = self.build_celex_url(metadata["CELEX number"])

            if metadata:
                self.metadata_list.append(metadata)

        metadata_dict = self.build_metadata_dict()
        standardized = standardize_metadata(metadata_dict)
        save_metadata_to_file(standardized, "metadata_eurlex.json")

    def collect_document_urls(self, url, driver=None):

        """
        Collects and returns a list of document URLs from a search results page.
        When this fails, an empty list is returned.
        """

        soup = self.get_soup(url)
        if not soup:
            return []

        document_urls = []
        for a in soup.find_all('a', href=True):
            if "/legal-content/EN/TXT/HTML/?" in a['href'] and "uri=CELEX:" in a['href']:
                document_urls.append(urljoin("https://eur-lex.europa.eu", a['href']))
        return document_urls
    
    def scrape_documents(self, document_urls):

        """
        Downloads and saves HTML content of documents from the given list of document URLs.
        Each document is saved locally using its CELEX number as filename.

        :param document_urls: List of document URLs to scrape
        """

        for url in document_urls:
            soup = self.get_soup(url)
            
            celex_number = self.extract_celex_number_from_url(url)

            if not celex_number:
                self.logger.error(f"Skipping document (CELEX number not found): {url}")
                continue

            with open(f"{celex_number}.html", "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))  # save HTML

            

