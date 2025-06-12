import os
import shutil
import pytest
import tempfile
import responses

from code.eur_lex.eur_lex_scraper import EurLexScraper

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "eurlex_sample.html")

@responses.activate
def test_eurlex_scraper_extracts_metadata_correctly():
    """
    Sanity test to ensure EurLexScraper still correctly extracts metadata from a search results page.
    """

    # This should match the URL you saved the fixture from
    url = "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=LEGISLATION&textScope0=ti-te&DTS_SUBDOM=LEGISLATION&DTS_DOM=EU_LAW&lang=en&type=advanced&date0=ALL%3A13122024%7C13022025&qid=1749741202686&andText0=sheep+wool"

    # Load your saved search results HTML
    with open(FIXTURE_PATH, encoding="utf-8") as f:
        html = f.read()

    # Intercept any HTTP GET to that URL and return the saved HTML
    responses.add(responses.GET, url, body=html, status=200)

    # Init scraper and run the metadata extractor
    scraper = EurLexScraper(base_url=url)
    scraper.extract_metadata(url)

    # Get the results
    metadata_list = scraper.metadata_list

    assert isinstance(metadata_list, list), "metadata_list should be a list"
    assert len(metadata_list) > 0, "No metadata entries were extracted"

    for item in metadata_list:
        assert isinstance(item, dict), "Each metadata item should be a dict"
        assert "CELEX number" in item and item["CELEX number"], "Missing or empty CELEX number"
        #assert "Title" in item and item["Title"], "Missing or empty Title"
        assert "url" in item and item["url"].startswith("https://"), "Missing or invalid URL"



