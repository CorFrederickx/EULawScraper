from scraper import BaseScraper
from european_parliament_think_thank.europarl_search import EuroparlSearch
from european_parliament_think_thank.europarl_scraper import EuroparlScraper

def scrape_docs (text, start_date='', end_date='',scrape=True, publication_types='', folder_path=''):

    text = input("Enter search text: ")
    start_date = input("Enter a start date (YYYYMMDD): ")
    end_date = input("Enter an end date (YYYYMMDD): ")
    folder_path = input("Enter folder to save files: ")

    # oude setup terugzetten

    folder_structure = {
        'folder_path': folder_path,
        'folders': [folder_path],
        'file_mapping': {".html": folder_path}
    }

    # saving the files


