from scraper import BaseScraper
from european_environment_agency.EEA_search import EEASearch
from european_environment_agency.EEA_scraper import EEAScraper

def scrape_docs():

    text = input("Enter search text: ")
    content_types = input("Enter content types: ")
    period = input("Enter time period: ")
    folder_path = input("Enter folder to save files: ")
    metadata_path = input("Enter path for metadata file: ")

    # OUDE SETUP TERUGZETTEN

    folder_structure = {
        'folder_path': folder_path,
        'metadata_path': metadata_path,
        'folders': [folder_path, metadata_path],
        'file_mapping': {".html": folder_path, ".json": metadata_path}
    }
    
    # saving the files

