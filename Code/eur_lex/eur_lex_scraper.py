import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import json

from scraper import BaseScraper
from .standardize_metadata_eurlex import standardize_metadata

class EurLexScraper(BaseScraper):

    def __init__(self, base_url):
        super().__init__(base_url)
        
        self.metadata_list = [] # list of dictionaries containing the metadata, later saved as JSON with celex numbers as keys
        self.documents = []

    def get_pagination_urls(self): # retrieve url of all the pages
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
    
    def extract_metadata(self, url): # extract metadata per document from a search result page
        soup = self.get_soup(url)

        if not soup:
            raise ValueError(f'No response for this URL: {url}')

        result_divs = soup.find_all('div', class_='SearchResultData collapse in')
        
        for div in result_divs:
            metadata = {}
            
            metadata_blocks = div.find_all('dl')
            
            for block in metadata_blocks:
                dt_elements = block.find_all('dt')
                dd_elements = block.find_all('dd')
                
                for dt, dd in zip(dt_elements, dd_elements):
                    key = dt.get_text(strip=True).replace(":", "")
                    value = dd.get_text(strip=True)
                    metadata[key] = value
            
            # get the legal status and add it to the metadata
            status_div = div.find_previous('div', class_='DocStatus')
            if status_div:
                status_text = status_div.get_text(strip=True)
                if "No longer in force" in status_text:
                    metadata["In force"] = False
                else:
                    metadata["In force"] = True

            # get the url and add it to the metadata
            if "CELEX number" in metadata:
                celex_number = metadata["CELEX number"]
                metadata['url'] = f'https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex_number}'

            if metadata:
                self.metadata_list.append(metadata)

        # convert metadata to the standard metadata format
        metadata_dict = {
            item["CELEX number"]: item
            for item in self.metadata_list if "CELEX number" in item
        }
        standard_metadata_dict = standardize_metadata(metadata_dict)

        # write metadata to JSON in current dir
        with open("metadata_eurlex.json", "w", encoding="utf-8") as f:
            json.dump(standard_metadata_dict, f, indent=4, ensure_ascii=False)

    def collect_document_urls(self, url): # extracts all the legal document urls from a given search results page.
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
            if soup:
                # extract CELEX number from URL
                celex_number = None
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                if "uri" in query_params:
                    celex_number = query_params["uri"][0].split(":")[-1]

            if not celex_number:
                print(f"Skipping document (CELEX number not found): {url}")
                continue
            
            with open(f"{celex_number}.html", "w", encoding="utf-8") as f:
                f.write(str(soup.prettify()))  # Save HTML

    def run(self, scrape=True):
        all_pages = self.get_pagination_urls()
        print(f"search results: total pages found: {len(all_pages)}")

        all_legislation_urls = []

        for page_url in all_pages:

            page_doc_urls = self.collect_document_urls(page_url)

            print(page_doc_urls)

            all_legislation_urls.extend(page_doc_urls)

            self.extract_metadata(page_url)
            
        print(f"Total legislation documents found: {len(all_legislation_urls)}")
        
        if scrape:
            print('Start scraping ')
            self.scrape_documents(all_legislation_urls)
            

