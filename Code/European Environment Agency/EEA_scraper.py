

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from selenium import webdriver
import time
import os
import json

from ..scraper import BaseScraper

class EEAScraper(BaseScraper):

    def __init__(self, base_url):
        super().__init__(base_url)

        self.metadata_list = []
    
    def get_pagination_urls(self, driver):

        driver.get(self.base_url)
        time.sleep(5) 

        try:
            # click the "Last page" button to reveal total number of pages
            last_page_btn = driver.find_element("css selector", "button[title='Last page']")
            last_page_btn.click()
            time.sleep(5) 

            # find the active page number (which is thus the last one)
            active_page_btn = driver.find_element("css selector", "button.pagination-item.active")
            total_pages = int(active_page_btn.text.strip())

            # Generate all paginated URLs based on base_url and total_pages
            paginated_urls = [f"{self.base_url}&page={page}" for page in range(1, total_pages + 1)]
            return paginated_urls

        except Exception as e:
            print(f"Just a single page: {e}")
            return [self.base_url]  # fallback to just the first page

    
    def collect_document_urls(self, url, driver):

        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup:
            return []
        
        unique_urls = set()

        h3_tags = soup.find_all('h3')
        if not h3_tags:
            print("No 'h3' tags with class 'listing-header' found on this page.")
        else:
            for h3 in h3_tags:
                a_tag = h3.find('a', href=True)
                if a_tag:
                    href = a_tag['href']
                    # print(f"Found URL: {href}")
                    unique_urls.add(href)

        # check if unique_urls contains any links
        if not unique_urls:
            print("No document URLs found on this page.")

        return list(unique_urls)

    def extract_metadata(self, url, driver):
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        if not soup:
            raise ValueError(f'No response for this URL: {url}')
        
        result_blocks = soup.find_all('div', class_='slot-bottom')
        
        for block in result_blocks:
            metadata = {}

            # get all result-info divs inside this block
            info_divs = block.find_all('div', class_='result-info')

            for div in info_divs:
                label_span = div.find('span', class_='result-info-title')
                if label_span:
                    label_text = label_span.get_text(strip=True)

                    # get the remaining text in the div after the label
                    full_text = div.get_text(strip=True).replace(label_text, '').strip()

                    if 'Topics:' in label_text:
                        metadata['Topics'] = full_text

                    elif 'Source:' in label_text:
                        a_tag = div.find('a', href=True)
                        if a_tag:
                            metadata['Source URL'] = a_tag['href']
                            strong_tag = a_tag.find('strong')
                            if strong_tag:
                                metadata['Source'] = strong_tag.get_text(strip=True)

                # fallback: assume if no label, it's the date
                elif not div.find('span'):
                    metadata['Date'] = div.get_text(strip=True)

            # get title and page URL from previous <h3>
            title_tag = block.find_previous('h3', class_='listing-header')
            if title_tag:
                a_tag = title_tag.find('a', href=True)
                if a_tag:
                    # Check for "New" label inside the <a>
                    new_label = a_tag.find('div', class_='ui label new-item')
                    if new_label:
                        metadata['Is New'] = True
                        new_label.extract()  # Remove it before getting the title text
                    else:
                        metadata['Is New'] = False

                    metadata['Title'] = a_tag.get_text(strip=True)
                    metadata['URL'] = a_tag['href']

            if metadata:
                self.metadata_list.append(metadata)

    def scrape_documents(self, document_urls, folder_path):
        
        # create folder if it does not exist
        os.makedirs(folder_path, exist_ok=True)

        for url in document_urls:
            soup = self.get_soup(url)
            if not soup:
                print(f"Skipping (no soup returned): {url}")
                continue

            # extract the last part of the URL path to use as filename
            parsed_url = urlparse(url)
            path_parts = parsed_url.path.rstrip('/').split('/')
            filename_base = path_parts[-1] if path_parts else "document"

            # clean filename if needed
            safe_filename = "".join(c if c.isalnum() or c in "-_." else "_" for c in filename_base)
            filepath = os.path.join(folder_path, f"{safe_filename}.html")

            # write as a HTML file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(soup.prettify())


    def run(self, metadata_path, folder_path, scrape=True):

        driver = webdriver.Chrome()

        all_pages = self.get_pagination_urls(self.driver)
        print(f"search results: total pages found: {len(all_pages)}")

        all_legislation_urls = []

        for page_url in all_pages:

            print(page_url)

            page_doc_urls = self.collect_document_urls(page_url, driver)

            print(f'page_doc_URLS: {page_doc_urls}')

            all_legislation_urls.extend(page_doc_urls)

            self.extract_metadata(page_url, driver)
            
        print(f"Total legislation documents found: {len(all_legislation_urls)}")

        metadata_dict = {item["Title"]: item for item in self.metadata_list if "Title" in item}
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, indent=4, ensure_ascii=False)
        
        if scrape:
            print('Start scraping ')
            self.scrape_documents(all_legislation_urls, folder_path=folder_path)

        driver.quit()

