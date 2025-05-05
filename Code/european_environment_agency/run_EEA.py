import os
from file_utils import FileManager
from scraper import BaseScraper
from european_environment_agency.EEA_search import EEASearch
from european_environment_agency.EEA_scraper import EEAScraper

def scrape_docs():

    text = input("Enter search text: ")
    content_types = input("Enter content types: ")
    period = input("Enter time period: ")
    folder_path = input("Enter folder to save files: ")
    metadata_path = input("Enter path for metadata file: ")

    search = EEASearch()
    search.set_text(text)
    search.set_content_type(content_types)
    search.set_time_period(period)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')
    
    scraper = EEAScraper(base_url)
    scraper.run()

    folder_structure = {
        'folders': [folder_path, metadata_path],
        'file_mapping': {".html": folder_path, ".json": metadata_path}
    }

    FileManager.create_folders(folder_structure['folders'])
    FileManager.move_files_to_folders(os.listdir(), folder_structure['file_mapping'])

    print(f"Scraped files saved in: {folder_path}")

