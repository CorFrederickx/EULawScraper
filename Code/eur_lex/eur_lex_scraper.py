import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import json

from scraper import BaseScraper
from .standardize_metadata_eurlex import standardize_metadata
from metadata_schema import save_metadata_to_file

class EurLexScraper(BaseScraper):

    # functions that determine how 'run' function in BaseClass is used
    def uses_driver(self):
        return False

    def has_pagination(self):
        return True

    def extracts_metadata(self):
        return True

    def __init__(self, base_url):
        super().__init__(base_url)
        
        self.metadata_list = [] # list of dictionaries containing the metadata, later saved as JSON with celex numbers as keys
        self.documents = []

    def get_pagination_urls(self, driver=None): # retrieve url of all the pages
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
        metadata = {}
        dt_elements = block.find_all('dt')
        dd_elements = block.find_all('dd')
        
        for dt, dd in zip(dt_elements, dd_elements):
            key = dt.get_text(strip=True).replace(":", "")
            value = dd.get_text(strip=True)
            metadata[key] = value
        return metadata
    
    def extract_legal_status(self, div):
        status_div = div.find_previous('div', class_='DocStatus')
        if status_div:
            status_text = status_div.get_text(strip=True)
            return not "No longer in force" in status_text
        return None

    # based on metadata this url can be built
    def build_celex_url(self, celex_number):
        return f'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex_number}'
    
    # function which does the opposite, extracts the celex from the url
    def extract_celex_number_from_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        if "uri" in query_params:
            return query_params["uri"][0].split(":")[-1]
        return None

    def build_metadata_dict(self):
        return {
            item["CELEX number"]: item
            for item in self.metadata_list if "CELEX number" in item
        }
    
    def extract_metadata(self, url, driver=None):
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
        soup = self.get_soup(url)
        if not soup:
            return []

        document_urls = []
        for a in soup.find_all('a', href=True):
            if "/legal-content/EN/TXT/HTML/?" in a['href'] and "uri=CELEX:" in a['href']:
                document_urls.append(urljoin("https://eur-lex.europa.eu", a['href']))
        return document_urls
    
    def scrape_documents(self, document_urls):

        for url in document_urls:
            soup = self.get_soup(url)
            
            celex_number = self.extract_celex_number_from_url(url)

            if not celex_number:
                print(f"Skipping document (CELEX number not found): {url}")
                continue
            
            with open(f"{celex_number}.html", "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))  # Save HTML
            

