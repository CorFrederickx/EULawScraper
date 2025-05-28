from urllib.parse import urlparse
import fitz
import tempfile
import os
import json

from scraper import BaseScraper
from .standardize_metadata_europarl import standardize_metadata
from metadata_schema import save_metadata_to_file

class EuroparlScraper(BaseScraper):

    # functions that determine how 'run' function in BaseClass is used
    def uses_driver(self):
        return False

    def has_pagination(self):
        return False

    def extracts_metadata(self):
        return True

    def __init__(self, base_url):
        super().__init__(base_url)
        
        self.metadata_list = []
        self.seen_document_ids = set()  # Set to track document IDs to avoid duplicates

    def save_temporary_pdf(self, content):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(content)
                print(f"Saved temporary file: {tmp_file.name}")
                return tmp_file.name
        except Exception as e:
            print(f"Error saving PDF to temporary file: {e}")
            return None
        
    def open_pdf_from_url(self, url):
        pdf_content = self.fetch_pdf_response(url)
        if not pdf_content:
            return None, None

        pdf_path = self.save_temporary_pdf(pdf_content)
        if not pdf_path:
            return None, None

        try:
            pdf_document = fitz.open(pdf_path)
            return pdf_document, pdf_path
        except Exception as e:
            print(f"Failed to open PDF: {e}")
            return None, None
    
    def extract_pdf_links(self, pdf_document):
        document_urls = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            for link in page.get_links():
                uri = link.get('uri')
                if uri and uri.lower().endswith('.pdf'):
                    document_urls.append(uri)
        return document_urls
    
    def remove_temporary_pdf(self, pdf_document, pdf_path):
        try:
            if pdf_document:
                pdf_document.close()
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception as e:
            print(f"Removal failed: {e}")


    def collect_document_urls(self, url, driver=None):

        pdf_document, pdf_path = self.open_pdf_from_url(url)

        if not pdf_document:
            return []

        try:
            return self.extract_pdf_links(pdf_document)
        except Exception as e:
            print(f"Error while processing PDF: {e}")
            return []
        finally:
            self.remove_temporary_pdf(pdf_document, pdf_path)

    # extracting the metadata:
    
    def extract_pdf_lines(self, pdf_document, skip_lines=9):
        full_text = "".join(page.get_text() for page in pdf_document)
        return full_text.strip().splitlines()[skip_lines:]

    
    def parse_metadata_from_lines(self, lines):
        metadata_list = []
        metadata = {}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if metadata.get("title") and line[0].isupper() and not line.startswith(
                ("Publication type", "Date", "External author", "Author", "Policy area", "Source")
            ):
                if "title" in metadata and "type" in metadata:
                    metadata_list.append(metadata)
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
                continue
            else:
                if metadata.get("title"):
                    metadata["title"] += " " + line
                else:
                    metadata["title"] = line

        if metadata and "title" in metadata and "type" in metadata:
            metadata_list.append(metadata)

        return metadata_list

    def extract_metadata(self, url, driver=None):

        pdf_document, pdf_path = self.open_pdf_from_url(url)
        if not pdf_document:
            return []

        try:
            lines = self.extract_pdf_lines(pdf_document, skip_lines=9)
        finally:
            self.remove_temporary_pdf(pdf_document, pdf_path)

        
        parsed_metadata = self.parse_metadata_from_lines(lines)
        self.metadata_list.extend(parsed_metadata)

        metadata_dict = {
            item["title"]: item
            for item in self.metadata_list if "title" in item
        }
        standard_metadata_dict = standardize_metadata(metadata_dict)
        save_metadata_to_file(standard_metadata_dict, "metadata_europarl.json")

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
                file_response = self.fetch_response(url)
                file_response.raise_for_status()
                with open(filename, "wb") as f:
                    f.write(file_response.content)

            except Exception as e:
                print(f"Failed to download {url}: {e}") 


        
    
