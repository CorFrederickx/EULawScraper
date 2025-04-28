
import os
from europarl_search import EuroparlSearch
from europarl_scraper import EuroparlScraper

def scrape_docs (text, start_date='', end_date='',scrape=True, publication_types='', folder_path=''):

    search = EuroparlSearch()
    search.set_text(text)
    search.set_date_range(start_date, end_date)
    search.set_publication_type(publication_types)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')

    # create folder if it does not exist
    os.makedirs(folder_path, exist_ok=True)
    
    scraper = EuroparlScraper(base_url)
    scraper.run(metadata_path='metadata.json', scrape=scrape)

    for file in os.listdir():
        if file.endswith(".pdf"):
            os.rename(file, os.path.join(folder_path, file))

    print(f'Scraped HTML files saved in: {folder_path}')