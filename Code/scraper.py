import requests
from bs4 import BeautifulSoup

class BaseScraper():
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
    
    # function to fetch and parse an html page
        
    def fetch_response(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return None
        
    def fetch_pdf_response(self, url):
        response = self.fetch_response(url)
        if not response:
            return []
        return response.content
    
    def get_soup(self, url):
        response = self.fetch_response(url)
        if response:
            return BeautifulSoup(response.text, 'html.parser')
        return None
    
    def download_file(self, url, filename):
        try:
            response = self.fetch_response(url)
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {filename}: {e}")


    # replacement of 'run' in each class:

    def run(self, scrape=True):
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
        all_urls = []

        for page_url in pages:
            print(f"Processing page: {page_url}")

            doc_urls = self.collect_document_urls(page_url, driver)
            print(f"Document URLs: {doc_urls}")

            all_urls.extend(doc_urls)

            if self.extracts_metadata():
                self.extract_metadata(page_url, driver)

        return list(set(all_urls))  # Remove duplicates



        

