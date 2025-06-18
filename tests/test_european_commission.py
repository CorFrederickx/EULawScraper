import os
import shutil
import pytest
import tempfile
import responses

from code.european_commission.european_commission_scraper import EuropeanCommissionScraper

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "european_commission_sample.html")

@responses.activate
def test_european_commission_scraper_single_page():
    """
    Tests the EuropeanCommissionScraper for document URL collection using only a single fixture page.
    """

    base_url = "https://ec.europa.eu/search/?queryText=fashion&query_source=europa_default&page=&filter=&swlang=en&filterSource=europa_default&more_options_date=-31&more_options_f_formats=*"

    with open(FIXTURE_PATH, encoding="utf-8") as f:
        html = f.read()

    responses.add(responses.GET, base_url, body=html, status=200)
    
    scraper = EuropeanCommissionScraper(base_url=base_url)
    
    doc_urls_page1 = scraper.collect_document_urls(base_url)

    expected_doc_urls_page1 = [
        "https://green-week.event.europa.eu/document/download/63482d24-231e-4f0a-8bf7-23098f991c76_en?filename=Programme_FFBS-Fashion%20For%20Biodiversity_v2.pdf",
        "https://green-week.event.europa.eu/document/download/36d80cb0-23fc-4fda-8b5d-c7c93ba6a606_en?filename=EU%20Green%20Week_FFW_Programme.pdf"
    ]
    assert sorted(doc_urls_page1) == sorted(expected_doc_urls_page1), \
        f"Expected document URLs {expected_doc_urls_page1}, got {doc_urls_page1}"