import requests
from urllib.parse import urlparse
import fitz
import tempfile
import os
import json

from scraper import BaseScraper
from .standardize_metadata_europarl import standardize_metadata

class EuroparlScraper(BaseScraper):

    def __init__(self, base_url):
        super().__init__(base_url)
        
        self.metadata_list = []
        self.seen_document_ids = set()  # Set to track document IDs to avoid duplicates
        
    def collect_document_urls(self, url):

        # download the pdf that is behind the url
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to download the PDF: {e}")
            return []

        # save it to a temporaryfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            pdf_path = tmp_file.name
            print(f"Saved temporary file: {pdf_path}")

        # extract the right hyperlinks using PyMuPDF
        document_urls = []
        try:
            pdf_document = fitz.open(pdf_path)

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                for link in page.get_links():
                    uri = link.get('uri')
                    if uri and uri.lower().endswith('.pdf'):
                        document_urls.append(uri)

        except Exception as e:
            print(f"Error while processing PDF: {e}")

        finally:
            pdf_document.close()
            os.remove(pdf_path)  # clean up the temporary file

        return document_urls
    
    def extract_metadata(self, url):
        # download the pdf that is behind the url
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to download the PDF: {e}")
            return []

        # save it to a temporaryfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(response.content)
            pdf_path = tmp_file.name
            print(f"Saved temporary file: {pdf_path}")

        pdf_document = fitz.open(pdf_path)
        full_text = ""
        for page in pdf_document:
            full_text += page.get_text()

        pdf_document.close()
        os.remove(pdf_path)

        lines = full_text.strip().splitlines()[9:]  # skip the first 9 lines (the stuff on the first page of the pdf)

        metadata = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # detect a new publication entry
            if metadata.get("title") and line[0].isupper() and not line.startswith(
                ("Publication type", "Date", "External author", "Author", "Policy area", "Source")
            ):
                if "title" in metadata and "type" in metadata:
                    self.metadata_list.append(metadata)
                metadata = {}

            if line.startswith("Publication type"):
                metadata["type"] = line.replace("Publication type", "").strip()

            elif line.startswith("Date"):
                metadata["date"] = line.replace("Date", "").strip()

            elif line.startswith("External author") or line.startswith("Author"):
                authors = line.split(" ", 1)[1].strip()
                metadata["authors"] = [author.strip() for author in authors.split(";")]

            elif line.startswith("Policy area"):
                metadata["policy_area"] = line.replace("Policy area", "").strip()

            elif line.startswith("Source"):
                continue  # skip footer lines

            else:
                # Assume it's the title
                if metadata.get("title"):
                    metadata["title"] += " " + line
                else:
                    metadata["title"] = line

        # add the last publication if any
        if metadata and "title" in metadata and "type" in metadata:
            self.metadata_list.append(metadata)

        # write metadata to JSON in current dir
        metadata_dict = {
            item["title"]: item
            for item in self.metadata_list if "title" in item
        }
        standard_metadata_dict = standardize_metadata(metadata_dict)

        with open("metadata_europarl.json", "w", encoding="utf-8") as f:
            json.dump(standard_metadata_dict, f, indent=4, ensure_ascii=False)

    def scrape_documents(self, document_urls):

        for url in document_urls:
            soup = self.get_soup(url)
            if soup:
                # extract filename from URL
                parsed_url = urlparse(url)
                path = parsed_url.path
                filename = os.path.basename(path)
                document_id = filename.split('_')[1]

                if document_id in self.seen_document_ids:
                    print(f"Skipping duplicate document (ID: {document_id}) - {filename}")
                    continue

                self.seen_document_ids.add(document_id)

            try:
                file_response = requests.get(url)
                file_response.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(file_response.content)

            except Exception as e:
                print(f"Failed to download {url}: {e}") 


    def run(self):

        self.extract_metadata(self.base_url)

        document_urls = self.collect_document_urls(self.base_url)
        document_urls = list(set(document_urls))

        print(f"Total downloadable documents found: {len(document_urls)}")

        print('Start scraping ')
        self.scrape_documents(document_urls)
        
    
