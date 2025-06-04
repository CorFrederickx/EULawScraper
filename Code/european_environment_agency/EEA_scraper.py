
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from selenium import webdriver
import time
import os
import json

from scraper import BaseScraper
from .standardize_metadata_eea import standardize_metadata
from metadata_schema import save_metadata_to_file

class EEAScraper(BaseScraper):

    logger = logging.getLogger(__name__)

    """
    Scraper class for extracting HTML documents and metadata from the European Environment Agency website, extending BaseScraper.
    """

    # functions that determine how 'run' function in BaseClass is used
    def uses_driver(self):

        """
        Indicates whether a WebDriver is required for scraping.
        The EEA website does indeed require a WebDriver.
        """

        return True
    
    def create_driver(self):

        """
        Returns a Selenium Chrome WebDriver instance for scraping dynamic EEA content.
        """

        return webdriver.Chrome()

    def has_pagination(self):

        """
        Indicates whether the search results are paginated.
        Pagination is present.
        """

        return True

    def extracts_metadata(self):

        """
        Indicates whether metadata extraction is supported.
        EEA supports metadata extraction.
        """

        return True

    def __init__(self, base_url):

        """
        Initializes an EEAScraper instance and prepares metadata storage.

        :param base_url: The base URL of the EEA search results page.
        """

        super().__init__(base_url)

        self.metadata_list = []
    
    def get_pagination_urls(self, driver):

        """
        Navigates through the EEA website using the given WebDriver: 
        Clicks the 'Last page' button to reveal the total number of result pages, 
        then constructs URLs for each page and returns them as a list. 
        Returns only the base URL if no last 'Last Page' button is found.
        """

        driver.get(self.base_url)
        time.sleep(5) 

        try:
            last_page_btn = driver.find_element("css selector", "button[title='Last page']")
            last_page_btn.click()
            time.sleep(5) 

            active_page_btn = driver.find_element("css selector", "button.pagination-item.active")
            total_pages = int(active_page_btn.text.strip())

            paginated_urls = [f"{self.base_url}&page={page}" for page in range(1, total_pages + 1)]
            return paginated_urls

        except Exception as e:
            self.logger.exception(f"Just a single page: {e}")
            return [self.base_url]  # fallback to just the first page

    
    def collect_document_urls(self, url, driver):

        """
        Extracts document URLs from a given search result page using the WebDriver, and returns them as a list.
        
        :param url: A search results page URL
        :param driver: A Selenium WebDriver instance
        """

        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup:
            return []
        
        unique_urls = set()

        h3_tags = soup.find_all('h3') # <h3> headers typically point to individual document pages
        if not h3_tags:
            self.logger.error("No 'h3' tags with class 'listing-header' found on this page.")
        else:
            for h3 in h3_tags:
                a_tag = h3.find('a', href=True)
                if a_tag:
                    href = a_tag['href']
                    # print(f"Found URL: {href}")
                    unique_urls.add(href)

        if not unique_urls:
            self.logger.info("No document URLs found on this page.")

        return list(unique_urls)
    
    def parse_result_block(self, block):

        """
        Parses a metadata <div> block containing fields such as 'Topics', 'Source', 'Source URL', and 'Date'
        into a dictionary of key-value pairs.

        :param block: A BeautifulSoup <div> element containing metadata
        :return: A dictionary of extracted metadata
        """

        metadata = {}
        info_divs = block.find_all('div', class_='result-info')

        for div in info_divs:
            label_span = div.find('span', class_='result-info-title')
            if label_span:
                label_text = label_span.get_text(strip=True)
                full_text = div.get_text(strip=True).replace(label_text, '').strip()

                if 'Topics:' in label_text:
                    metadata['Topics'] = full_text
                elif 'Source:' in label_text:
                    a_tag = div.find('a', href=True)
                    if a_tag:
                        metadata['Source URL'] = a_tag['href']
                        strong_tag = a_tag.find('strong')
                        if strong_tag:
                            metadata['Source'] = strong_tag.get_text(strip=True)
            elif not div.find('span'):
                metadata['Date'] = div.get_text(strip=True)

        return metadata
    
    def parse_title_metadata(self, block):

        """
        Parses a metadata <div> block containing title-related metadata,
        such as 'Title text', 'Document URL or whether the document is labeled as 'new', into a dictionary of key-value pairs.

        :param block: A BeautifulSoup <div> element containing metadata
        :return: A dictionary of extracted metadata
        """

        metadata = {}
        title_tag = block.find_previous('h3', class_='listing-header')
        if title_tag:
            a_tag = title_tag.find('a', href=True)
            if a_tag:
                new_label = a_tag.find('div', class_='ui label new-item')
                metadata['Is New'] = bool(new_label)
                if new_label:
                    new_label.extract()
                metadata['Title'] = a_tag.get_text(strip=True)
                metadata['URL'] = a_tag['href']
        return metadata


    def extract_metadata(self, url, driver):

        """
        Combines `parse_result_block` and `parse_title_metadata` to extract metadata from an EEA search results page.
        The metadata is then standardized and saved to a local file named 'metadata_eea.json'.

        :param url: The URL of the search result page to extract metadata from
        :param driver: A Selenium WebDriver instance
        """
        
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if not soup:
            raise ValueError(f'No response for this URL: {url}')
        
        result_blocks = soup.find_all('div', class_='slot-bottom')

        for block in result_blocks:
            metadata = self.parse_result_block(block)
            metadata.update(self.parse_title_metadata(block))

            if metadata:
                self.metadata_list.append(metadata)

        metadata_dict = {
            item["Title"]: item
            for item in self.metadata_list if "Title" in item
        }

        standardized = standardize_metadata(metadata_dict)
        save_metadata_to_file(standardized, "metadata_eea.json")

    def scrape_documents(self, document_urls):

        """
        Downloads and saves the HTML content of documents listed in the provided URLs.

        :param document_urls: List of URLs pointing to individual documents
        """

        for url in document_urls:
            soup = self.get_soup(url)
            if not soup:
                self.logger.info(f"Skipping (no soup returned): {url}")
                continue

            # last part of the URL as filename
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.rstrip('/').split('/')
            filename_base = path_parts[-1] if path_parts else "document"

            safe_filename = "".join(c if c.isalnum() or c in "-_." else "_" for c in filename_base)
            filepath = os.path.join(".", f"{safe_filename}.html")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(soup.prettify())

