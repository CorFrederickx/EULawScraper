import os
import pytest
from unittest.mock import MagicMock

from code.european_environment_agency.EEA_scraper import EEAScraper

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "eea_sample.html")

def test_eea_scraper_extracts_metadata_correctly():
    """
    Sanity test to ensure EEAScraper correctly extracts metadata from a sample EEA HTML page.
    """

    with open(FIXTURE_PATH, encoding="utf-8") as f:
        html = f.read()

    # create a mock Selenium driver
    mock_driver = MagicMock()
    mock_driver.page_source = html

    # this should match the URL you saved the fixture from (not used since we're mocking driver behavior)
    url = "https://www.eea.europa.eu/en/advanced-search?q=fashion&size=n_10_n&filters%5B0%5D%5Bfield%5D=readingTime&filters%5B0%5D%5Bvalues%5D%5B0%5D%5Bname%5D=All&filters%5B0%5D%5Bvalues%5D%5B0%5D%5BrangeType%5D=fixed&filters%5B0%5D%5Btype%5D=any&filters%5B1%5D%5Bfield%5D=issued.date&filters%5B1%5D%5Bvalues%5D%5B0%5D=Last%203%20months&filters%5B1%5D%5Btype%5D=any&filters%5B2%5D%5Bfield%5D=objectProvides&filters%5B2%5D%5Bvalues%5D%5B0%5D=Briefing&filters%5B2%5D%5Bvalues%5D%5B1%5D=Article&filters%5B2%5D%5Btype%5D=any"

    # Initialize the scraper
    scraper = EEAScraper(base_url=url)

    # Run metadata extraction
    scraper.extract_metadata(url=url, driver=mock_driver)

    metadata_list = scraper.metadata_list

    assert isinstance(metadata_list, list), "metadata_list should be a list"
    assert len(metadata_list) > 0, "No metadata entries were extracted"

    for item in metadata_list:
        assert isinstance(item, dict), "Each metadata item should be a dict"
        assert "Title" in item and item["Title"], "Missing or empty Title"
        assert "URL" in item and item["URL"].startswith("http"), "Missing or invalid URL"
