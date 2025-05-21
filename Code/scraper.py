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



        

