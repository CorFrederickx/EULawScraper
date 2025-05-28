"""Promting user for criteria. Searching and scraping based on those"""

import os
from file_utils import FileManager
from european_commission.european_commission_search import EuropeanCommissionSearch
from european_commission.european_commission_scraper import EuropeanCommissionScraper

def scrape_docs():

    """
    Asks the user for search criteria and destination folder.
    Then uses `EuropeanCommissionSearch` to build a search URL based on user input, and `EuropeanCommissionScraper` to scrape the found documents.
    Downloaded files are organized into the right folders using the `FileManager` class.  
    """

    text = input("Enter search text: ")
    period = input("Enter time period: ")
    folder_path = input("Enter folder to save files: ")
    format = input("Enter format: ")

    pdf_folder = os.path.join(folder_path, "pdf")
    doc_folder = os.path.join(folder_path, "doc")
    xlsx_folder = os.path.join(folder_path, "xlsx")
    txt_folder = os.path.join(folder_path, "txt")
    ppt_folder = os.path.join(folder_path, "ppt")

    search = EuropeanCommissionSearch()
    search.set_text(text)
    search.set_date(period)
    search.set_format(format)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')

    scraper = EuropeanCommissionScraper(base_url)
    scraper.run()

    folder_structure = {
        'folders': [pdf_folder, doc_folder, xlsx_folder, txt_folder, ppt_folder],
        'file_mapping': {".PDF": pdf_folder, ".pdf": pdf_folder, ".docx": doc_folder, ".xlsx": xlsx_folder, ".txt":txt_folder, ".pptx": ppt_folder}
    }

    FileManager.create_folders(folder_structure['folders'])
    FileManager.move_files_to_folders(os.listdir(), folder_structure['file_mapping'])

    print(f"Scraped files saved in: {folder_path}")
    



