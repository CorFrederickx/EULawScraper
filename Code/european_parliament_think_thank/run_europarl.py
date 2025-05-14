import os
from file_utils import FileManager
from european_parliament_think_thank.europarl_search import EuroparlSearch
from european_parliament_think_thank.europarl_scraper import EuroparlScraper

def scrape_docs ():
    
    text = input("Enter search text: ")
    start_date = input("Enter a start date (DDMMYYYY): ")
    end_date = input("Enter an end date (DDMMYYYY): ")
    publication_types = input("Enter publication types: ")
    folder_path = input("Enter folder to save files: ")
    metadata_path = input("Enter path for metadata file: ")

    search = EuroparlSearch()
    search.set_text(text)
    search.set_date_range(start_date, end_date)
    search.set_publication_type(publication_types)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')

    scraper = EuroparlScraper(base_url)
    scraper.run()

    folder_structure = {
        'folders': [folder_path, metadata_path],
        'file_mapping': {".pdf": folder_path, ".json": metadata_path}
    }

    FileManager.create_folders(folder_structure['folders'])
    FileManager.move_files_to_folders(os.listdir(), folder_structure['file_mapping'])

    print(f"Scraped files saved in: {folder_path}")



