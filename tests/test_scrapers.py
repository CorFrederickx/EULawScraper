import os
import shutil
import pytest
import tempfile
import responses


from code.eur_lex.eur_lex_scraper import EurLexScraper
from code.european_commission.european_commission_scraper import EuropeanCommissionScraper
from code.european_environment_agency.EEA_scraper import EEAScraper
from code.european_parliament_think_thank.europarl_scraper import EuroparlScraper

PLATFORMS = [
    {
        "name": "eurlex",
        "scraper_cls": EurLexScraper,
        "url": "https://eur-lex.europa.eu/search.html?SUBDOM_INIT=LEGISLATION&textScope0=ti-te&DTS_SUBDOM=LEGISLATION&DTS_DOM=EU_LAW&lang=en&type=advanced&date0=ALL%3A13122024%7C13022025&qid=1749741202686&andText0=sheep+wool",
        "fixture": "eurlex_sample.html",
    },
    {
        "name": "european_commission",
        "scraper_cls": EuropeanCommissionScraper,
        "url": "https://food.ec.europa.eu/document/download/ef30c51c-331d-4d88-ab3b-2a2497d73009_en?filename=ia_standards_oie_eu_position_tahsc-report_202502_annex-1.pdf",
        "fixture": "european_commission_sample.pdf"
    },
    {
        "name": "eea",
        "scraper_cls": EEAScraper,
        "url": "https://www.eionet.europa.eu/etcs/etc-ce/products/etc-ce-report-2025-8-a-just-transition-to-circular-economy",
        "fixture": "eea_sample.html"
    },
    {
        "name": "europarl",
        "scraper_cls": EuroparlScraper,
        "url": "https://www.europarl.europa.eu/RegData/etudes/BRIE/2025/767204/EPRS_BRI(2025)767204_EN.pdf",
        "fixture": "europarl_sample.pdf"
    }
]

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.mark.parametrize("cfg", PLATFORMS, ids=[p["name"] for p in PLATFORMS])
@responses.activate

def test_scraper(cfg):

    """
    Sanity check whether scraper outputs expected result (fixture)
    """

    fixture_path = os.path.join(FIXTURE_DIR, cfg["fixture"])
    is_pdf = fixture_path.endswith(".pdf")
    mode = "rb" if is_pdf else "r"
    content_type = "application/pdf" if is_pdf else "text/html"

    with open(fixture_path, mode) as f:
        fixture_content = f.read()

    responses.add(responses.GET, cfg["url"], body=fixture_content, content_type=content_type)

    temp_dir = tempfile.mkdtemp()
    try:
        scraper = cfg["scraper_cls"]()
        scraper.output_dir = temp_dir
        scraper.scrape_documents([cfg["url"]])

        saved_files = os.listdir(temp_dir)
        assert saved_files, "No files saved by scraper"

        for filename in saved_files:
            with open(os.path.join(temp_dir, filename), "rb") as sf:
                saved_content = sf.read()
                assert saved_content == fixture_content, f"Saved file {filename} content does not match fixture"

    finally:
        shutil.rmtree(temp_dir)


