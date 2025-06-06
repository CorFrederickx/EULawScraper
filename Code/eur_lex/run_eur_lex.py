"""Promting user for criteria. Searching and scraping based on those"""
import logging
import os
from file_utils import FileManager
from eur_lex.eur_lex_search import EurLexSearch
from eur_lex.eur_lex_scraper import EurLexScraper

logger = logging.getLogger(__name__)

def scrape_docs():

    """
    Asks the user for search criteria and a destination folder.
    Then uses `EurLexSearch` to build a search URL based on user input, and `EurLexScraper` to scrape the found documents and corresponding metadata.
    Downloaded files and their metadata are organized into the right folders using the `FileManager` class.  
    """

    collections= input("Enter collection(s): ")
    text = input("Enter search text: ")
    start_date = input("Enter a start date (DDMMYYYY): ")
    end_date = input("Enter an end date (DDMMYYYY) (make it the same as the start date if looking for a specific date): ")
    folder_path = input("Enter folder to save files: ")
    metadata_path = input("Enter path for metadata file: ")

    search = EurLexSearch()
    search.set_collection(collections)
    search.set_first_text(text)
    search.set_date_range('ALL', start_date, end_date)
    
    base_url = search.build()
    logger.info(f'the search results page is: {base_url}')

    scraper = EurLexScraper(base_url)
    scraper()

    folder_structure = {
        'folders': [folder_path, metadata_path],
        'file_mapping': {".html": folder_path, ".json": metadata_path}
    }

    FileManager.create_folders(folder_structure['folders'])
    FileManager.move_files_to_folders(os.listdir(), folder_structure['file_mapping'])

    logger.info(f"Scraped files saved in: {folder_path}")
