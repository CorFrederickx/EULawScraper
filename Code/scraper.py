import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

class BaseScraper():
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"User-Agent": "Mozilla/5.0"}
    
    # function to fetch and parse an html page
    def get_soup(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    # kunnen deze functies beter elders staan?
    
    def create_folders(folders):
        for folder in folders:
            os.makedirs(folder, exist_ok=True)

    def move_files_to_folders(files, folder_mapping):
        for file in files:
            for extension, folder in folder_mapping.items():
                if file.endswith(extension):
                    shutil.move(file, os.path.join(folder, file))

        

