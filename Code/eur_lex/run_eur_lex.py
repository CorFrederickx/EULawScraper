import os
from file_utils import FileManager
from scraper import BaseScraper
from eur_lex.eur_lex_search import GetAdvancedSearchURL
from eur_lex.eur_lex_scraper import EurLexScraper

def scrape_docs():

    collections= input("Enter collection(s): ")
    text = input("Enter search text: ")
    start_date = input("Enter a start date (DDMMYYYY): ")
    end_date = input("Enter an end date (DDMMYYYY) (make it the same as the start date if looking for a specific date): ")
    folder_path = input("Enter folder to save files: ")
    metadata_path = input("Enter path for metadata file: ")

    search = GetAdvancedSearchURL()
    search.set_collection(collections)
    search.set_first_text(text)
    search.set_date_range('ALL', start_date, end_date)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')

    scraper = EurLexScraper(base_url)
    scraper.run()

    folder_structure = {
        'folders': [folder_path, metadata_path],
        'file_mapping': {".html": folder_path, ".json": metadata_path}
    }

    FileManager.create_folders(folder_structure['folders'])
    FileManager.move_files_to_folders(os.listdir(), folder_structure['file_mapping'])

    print(f"Scraped files saved in: {folder_path}")
