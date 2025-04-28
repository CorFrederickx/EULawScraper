import os
import shutil
from european_commission_search import EuropeanCommissionSearch
from european_commission_scraper import EuropeanCommissionScraper

def scrape_docs (text, period, folder_path, format, scrape=True):

    search = EuropeanCommissionSearch()
    search.set_text(text)
    search.set_date(period)
    search.set_format(format)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')

    # create folder if it does not exist
    os.makedirs(folder_path, exist_ok=True)

    # define subfolders
    pdf_folder = os.path.join(folder_path, "pdfs")
    doc_folder = os.path.join(folder_path, "docs")
    xlsx_folder = os.path.join(folder_path, "excels")
    txt_folder = os.path.join(folder_path, "texts")
    ppt_folder = os.path.join(folder_path, "ppts")

    # create subfolders if they don't exist
    for subfolder in [pdf_folder, doc_folder, xlsx_folder, txt_folder, ppt_folder]:
        os.makedirs(subfolder, exist_ok=True)
    
    scraper = EuropeanCommissionScraper(base_url)
    scraper.run(scrape=scrape)

    # move the scraped files into specified folders
    for file in os.listdir():
        if file.endswith(".pdf"):
            shutil.move(file, os.path.join(pdf_folder, file))
        elif file.endswith(".doc"):
            shutil.move(file, os.path.join(doc_folder, file))
        elif file.endswith(".xlsx"):
            shutil.move(file, os.path.join(xlsx_folder, file))
        elif file.endswith(".txt"):
            shutil.move(file, os.path.join(txt_folder, file))
        elif file.endswith(".ppt"):
            shutil.move(file, os.path.join(ppt_folder, file))

    # remove empty folders
    for folder in [pdf_folder, doc_folder, xlsx_folder, txt_folder, ppt_folder]:
        if not os.listdir(folder):
            os.rmdir(folder)


    print(f'Scraped files saved in: {folder_path} and its subfolders')