from scraper import BaseScraper
from european_commission.european_commission_search import EuropeanCommissionSearch
from european_commission.european_commission_scraper import EuropeanCommissionScraper

def scrape_docs (text, period, folder_path, format, scrape=True):

    text = input("Enter search text: ")
    period = input("Enter time period: ")
    folder_path = input("Enter folder to save files: ")
    format = input("Enter format: ")

    # NOG TERUG AAN TE PASSEN NAAR OUDE SETUP

    folder_structure = {
        'folder_path': folder_path,
        'folders': [pdf_folder, doc_folder, xlsx_folder, txt_folder, ppt_folder],
        'file_mapping': {".pdf": pdf_folder, ".docx": doc_folder, ".xlsx": xlsx_folder, ".txt":txt_folder, ".pptx": ppt_folder}
    }


