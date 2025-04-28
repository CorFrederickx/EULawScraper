import os
from search_url_builder import GetAdvancedSearchURL
from eur_lex_scraper import EurLexScraper


def scrape_htmls (collection, text, start_date, end_date, folder_path, metadata_path, scrape=True):

    search = GetAdvancedSearchURL()
    search.set_collection(collection)
    search.set_text(text)
    search.set_date_range('ALL', start_date, end_date)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')

    # create folder if it does not exist
    os.makedirs(folder_path, exist_ok=True)
    
    scraper = EurLexScraper(base_url)
    scraper.run(metadata_path, scrape=scrape)

    # move the scraped HTML files to the specified folder
    for file in os.listdir():
        if file.endswith(".html"):
            os.rename(file, os.path.join(folder_path, file))

    print(f'Scraped HTML files saved in: {folder_path}')
    print(f'Metadata saved in: {metadata_path}')