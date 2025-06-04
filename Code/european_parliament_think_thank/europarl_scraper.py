from urllib.parse import urlparse
import fitz
import tempfile
import os
import json

from scraper import BaseScraper
from .standardize_metadata_europarl import standardize_metadata
from metadata_schema import save_metadata_to_file

class EuroparlScraper(BaseScraper):

    """
    Scraper class for extracting PDF documents and metadata from the Europarl website, extending BaseScraper.

    Europarl is special in that a search results page consists of a PDF that lists all the found documents.
    """

    def uses_driver(self):

        """
        Indicates whether a WebDriver is required for scraping.
        Europarl does not require a WebDriver.
        """

        return False
    
    def create_driver(self):

        """
        Returns None since this scraper does not require a WebDriver.
        """

        return None

    def has_pagination(self):

        """
        Indicates whether the search results are paginated
        Europarl pages are not paginated. Instead, all results are listed in one pdf document.
        """

        return False

    def extracts_metadata(self):

        """
        Indicates whether metadata can be extracted for each document.
        Europarl supports metadata extraction.
        """

        return True

    def __init__(self, base_url):

        """
        Initializes a EuroparlScraper instance and prepares metadata storage.

        :param base_url: The base URL for the Europarl search results page, which comes as a pdf itself.
        """

        super().__init__(base_url)
        
        self.metadata_list = []
        self.seen_document_ids = set()  # set to track document IDs to avoid duplicates/translations when scraping

    def save_temporary_pdf(self, content):

        """
        Saves PDF content to a temporary file on disk and returns the path to this file, or None if saving fails.

        :param content: Content of a PDF file.
        """

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(content)
                self.logger.info(f"Saved temporary file: {tmp_file.name}")
                return tmp_file.name
        except Exception as e:
            self.logger.exception(f"Error saving PDF to temporary file: {e}")
            return None
        
    def open_pdf_from_url(self, url):

        """
        Downloads the search results PDF from the given base URL,
        saves it as a temporary file and opens it using PyMuPDF (fitz).

        :return: Tuple of (PDF document object, file path) or (None, None) on failure.
        """

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

        """
        Extracts direct PDF URLs embedded within the pages of an already opened PDF document.
        
        :param pdf_document: A PyMuPDF document object (opened and ready for reading).
        :return: List of URLs (strings) found within the document that end in '.pdf'.
        """

        document_urls = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            for link in page.get_links():
                uri = link.get('uri')
                if uri and uri.lower().endswith('.pdf'):
                    document_urls.append(uri)
        return document_urls
    
    def remove_temporary_pdf(self, pdf_document, pdf_path):

        """
        Closes the temporary PDF document and removes it.

        :param pdf_document: PyMuPDF document object.
        :param pdf_path: Path to the temporary PDF file.
        """

        try:
            if pdf_document:
                pdf_document.close()
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
        except Exception as e:
            self.logger.exception(f"Removal failed: {e}")


    def collect_document_urls(self, url, driver=None):

        """
        Downloads and opens a PDF from the given URL, then extracts embedded PDF links from it using `extract_pdf_links`.
        
        :param url: The web URL pointing to a PDF file that contains links to other PDFs.
        :return: List of extracted PDF URLs found within the downloaded document.
        """

        pdf_document, pdf_path = self.open_pdf_from_url(url)

        if not pdf_document:
            return []

        try:
            return self.extract_pdf_links(pdf_document)
        except Exception as e:
            self.logger.exception(f"Error while processing PDF: {e}")
            return []
        finally:
            self.remove_temporary_pdf(pdf_document, pdf_path)

    # extracting the metadata:
    
    def extract_pdf_lines(self, pdf_document, skip_lines=9):

        """
        Extracts text from a PDF document, skipping a specified number of header lines.

        :param pdf_document: PyMuPDF document.
        :param skip_lines: Number of lines to skip at the beginning.
        :return: List of text lines from the document.
        """

        full_text = "".join(page.get_text() for page in pdf_document)
        return full_text.strip().splitlines()[skip_lines:]

    
    def parse_metadata_from_lines(self, lines):

        """
        Parses metadata entries from a list of text lines.

        :param lines: List of text lines extracted from a PDF.
        :return: List of metadata dictionaries.
        """

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

        """
        Extracts metadata from a PDF document located at the given URL,
        then standardizes and saves it to a JSON file.
        """

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

    def extract_filename_and_id(self, url):
        
        """
        Extracts the filename and document ID from a given URL.
        Assumes the document ID is the second element when the filename is split by '_'.

        :param url: The document URL.
        :return: Tuple (filename, document_id).
        """

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        parts = filename.split('_')
        document_id = parts[1] if len(parts) > 1 else None
        return filename, document_id


    def scrape_documents(self, document_urls):

        """
        Downloads and saves PDF documents from a list of URLs, avoiding duplicates using document IDs.

        :param document_urls: List of PDF download URLs.
        """

        for url in document_urls:
            soup = self.get_soup(url)
            if soup:
                filename, document_id = self.extract_filename_and_id(url)

                if document_id in self.seen_document_ids:
                    self.logger.info(f"Skipping duplicate document (ID: {document_id}) - {filename}")
                    continue

                self.seen_document_ids.add(document_id)
                self.download_file(url, filename)


        
    
