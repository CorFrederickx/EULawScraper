
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

from scraper import BaseScraper

class EuropeanCommissionScraper(BaseScraper):

    # functions that determine how 'run' function in BaseClass is used
    def uses_driver(self):
        return False

    def has_pagination(self):
        return True

    def extracts_metadata(self):
        return False

    def __init__(self, base_url):
        super().__init__(base_url)
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
        
    def get_pagination_urls(self, driver=None):
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

        print(paginated_urls)
        return paginated_urls

    
    def collect_document_urls(self, url, driver=None):

        soup = self.get_soup(url)
        if not soup:
            return []
        
        unique_urls = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "document/download/" in href:
                full_url = urljoin(url, href)  # handle relative URLs
                unique_urls.add(full_url)
            
        return list(unique_urls)
    
    def extract_filename_from_url(self, url):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("filename", [None])[0]

    def scrape_documents(self, document_urls):
        
        for url in document_urls:
            filename = self.extract_filename_from_url(url)
            if not filename:
                print(f"Filename not found in URL: {url}")
                continue
            self.download_file(url, filename)

