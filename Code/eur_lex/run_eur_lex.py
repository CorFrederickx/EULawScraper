from scraper import BaseScraper
from eur_lex.eur_lex_search import GetAdvancedSearchURL
from eur_lex.eur_lex_scraper import EurLexScraper

def scrape_htmls():

    collections= input("Enter collection(s): ")
    text = input("Enter search text: ")
    start_date = input("Enter a start date (YYYYMMDD): ")
    end_date = input("Enter an end date (YYYYMMDD) (make it the same as the start date if looking for a specific date): ")
    folder_path = input("Enter folder to save files: ")
    metadata_path = input("Enter path for metadata file: ")

# NOG TERUG AAN TE PASSEN NAAR OUDE SETUP

    folder_structure = {
        'folder_path': folder_path,
        'metadata_path': metadata_path,
        'folders': [folder_path, metadata_path],
        'file_mapping': {".html": folder_path, ".json": metadata_path}
    }

    # Dit volgende in een baseclass stuken?
    if folder_structure:
        create_folders(folder_structure["folders"])
        move_files_to_folders(os.listdir(), folder_structure["file_mapping"])
        
        print(f"Scraped files saved in: {folder_structure['folder_path']}")
