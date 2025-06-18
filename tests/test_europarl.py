import os
import shutil
import pytest
import tempfile
import responses
import fitz

from code.european_parliament_think_thank.europarl_scraper import EuroparlScraper

# Path to your sample Europarl search results PDF fixture
FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "europarl_sample.pdf")

@responses.activate
def test_europarl_scraper_extracts_metadata_correctly():
    """
    Sanity test to ensure EuroparlScraper correctly extracts metadata from a sample PDF in fixtures.
    """

    # this should match the URL you saved the fixture from
    url = "https://www.europarl.europa.eu/thinktank/en/research/advanced-search/pdf?textualSearch=sheep+wool&startDate=13%2F12%2F2024&endDate=13%2F02%2F2025&publicationTypes=AT_A_GLANCE"

    with open(FIXTURE_PATH, "rb") as f:
        pdf_content = f.read()

    responses.add(responses.GET, url, body=pdf_content, status=200, content_type='application/pdf')

    scraper = EuroparlScraper(base_url=url)
    scraper.extract_metadata(url)

    metadata_list = scraper.metadata_list

    assert isinstance(metadata_list, list), "metadata_list should be a list"
    assert len(metadata_list) > 0, "No metadata entries were extracted"

    for item in metadata_list:
        assert isinstance(item, dict), "Each metadata item should be a dict"
        assert "title" in item and item["title"], "Missing or empty title"
        assert "type" in item and item["type"], "Missing or empty type"
        assert "date" in item and item["date"], "Missing or empty date"
        assert "authors" in item and isinstance(item["authors"], list), "Missing or invalid authors"
        assert "policy_area" in item and item["policy_area"], "Missing or empty policy area"