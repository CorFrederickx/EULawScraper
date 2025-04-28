
from EEA_advanced_search import EEASearch
from EEA_scraper import EEAScraper

def scrape_docs (text, content_types='', time_period='Last 5 years',  folder_path="html_pages", metadata_path='metadata.json', scrape=True):

    search = EEASearch()
    search.set_text(text)
    search.set_time_period(time_period)
    search.set_content_type(content_types)
    
    base_url = search.build()
    print(f'the search results page is: {base_url}')
    
    scraper = EEAScraper(base_url)
    scraper.run(folder_path=folder_path, metadata_path=metadata_path, scrape=scrape)

    print(f'Scraped files saved in {folder_path}')