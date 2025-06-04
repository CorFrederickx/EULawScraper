"""Promting user for criteria. Searching and scraping based on those"""

import logging
import os
from file_utils import FileManager
from scraper import BaseScraper
from european_environment_agency.EEA_search import EEASearch
from european_environment_agency.EEA_scraper import EEAScraper

def scrape_docs():

    logger = logging.getLogger(__name__)

    """
    Asks the user for search criteria and destination folder.
    Then uses `EEASearch` to build a search URL based on user input, and `EEAScraper` to scrape the found documents and corresponding metadata.
    Downloaded files and their metadata are organized into the right folders using the `FileManager` class.  
    """

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
    logger.info(f'the search results page is: {base_url}')
    
    scraper = EEAScraper(base_url)
    scraper()

    folder_structure = {
        'folders': [folder_path, metadata_path],
        'file_mapping': {".html": folder_path, ".json": metadata_path}
    }

    FileManager.create_folders(folder_structure['folders'])
    FileManager.move_files_to_folders(os.listdir(), folder_structure['file_mapping'])

    logger.info(f"Scraped files saved in: {folder_path}")

