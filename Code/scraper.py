"""scraping documents from the found search results pages"""

import requests
from bs4 import BeautifulSoup

class BaseScraper():

    """Abstract base class for scraping found legislation"""

    def __init__(self, base_url):

        """
        Initialize an instance of the scraper with a base_url

        :param base_url: The URL of the search results page that was build by the BaseSearchURL class.
        """
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
    
    # function to fetch and parse an html page
        
    def fetch_response(self, url):

        """Fetches and returns the HTTP response object for a given URL. If the request fails, it returns None"""

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return None
        
    def fetch_pdf_response(self, url):

        """
        If the HTTP response object of given URL is valid, the content of the response is returned. If not, an empty list is returned.
        Used in europarl_scraper.py, where content consists of the binary data of a PDF.
        """

        response = self.fetch_response(url)
        if not response:
            return []
        return response.content
    
    def get_soup(self, url):

        """Turns the HTTP response object of given URL into a BeautifulSoup object for parsing HTML content."""

        response = self.fetch_response(url)
        if response:
            return BeautifulSoup(response.text, 'html.parser')
        return None
    
    def download_file(self, url, filename):

        """
        Downloads a file from given URL and saves it locally under given filename.
        If successful, a confirmation message is printed. Any error occuring is catched as an exception and an error message is printed.
        Used in european_commission_scraper.py only. (Should it be moved there?)
        """

        try:
            response = self.fetch_response(url)
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")


    # two functions that combine all functions in a scraper class:

    """It initializes a web driver if needed,
    collects URLs from paginated pages, gathers all document URLs, and optionally scrapes the documents.
    It ensures that the web driver is properly closed after the process is complete.

    Args:
        scrape (bool, optional): A flag indicating whether to perform the scraping of documents.
                                Defaults to True.

    Returns:
        None
    """

    def run(self, scrape=True):
        """
        Executes the scraping process.
        Initializes a webdriver, collects URLs from paginated pages and URLs of all documents on those pages and associated metadata. The documents are the scraped.
        Whether a step in this process is necessary is defined by sub-class functions:
            - uses_driver()
            - has_pagination()
            - extracts_metadata()
        """

        driver = self.create_driver() if self.uses_driver() else None

        try:
            pages = self.get_pagination_urls(driver if self.uses_driver() else None) if self.has_pagination() else [self.base_url]
            print(f"Total pages: {len(pages)}")

            all_urls = self.collect_all_document_urls(pages, driver)
            print(f"Total downloadable documents found: {len(all_urls)}")

            if scrape:
                print("Start scraping")
                self.scrape_documents(all_urls)

        finally:
            if driver:
                driver.quit()


    def collect_all_document_urls(self, pages, driver=None):
        
        """
        Helper function for 'run': iterates over each page URL, collects document URLs from each page and finally returns a list of unique document URLs
        Optionally metadata is extracted, depending on the extracts_metadata() function in the associated subclass.
        """

        all_urls = []

        for page_url in pages:
            print(f"Processing page: {page_url}")

            doc_urls = self.collect_document_urls(page_url, driver)
            print(f"Document URLs: {doc_urls}")

            all_urls.extend(doc_urls)

            if self.extracts_metadata():
                self.extract_metadata(page_url, driver)

        return list(set(all_urls)) 



        

