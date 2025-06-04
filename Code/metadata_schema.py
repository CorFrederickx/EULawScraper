import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def get_standard_metadata_template():

    """
    Returns a standardized metadata template that unifies metadata fields across the EUR-Lex, EEA and Europarl websites.

    This schema is filled in by running the `standardize_metadata_x.py` files, 
    which is done in the `extract_metadata` functions that are in every scraper class of the mentioned websites.
    """



    return {
        "id": None,                                # e.g., CELEX number or document title
        "title": None,                             # Title of the document (Europarl)
        "form": None,                              # Regulation, Decision, etc. (EUR-Lex: "Form")
        "type": None,                              # Document type (Europarl: "type")
        "author": None,                            # Single string or list of authors
        "date": None,                              # Date of document
        "status": None,                            # "In force" as boolean, Eur-Lex specific
        "policy_area": None,                       # Europarl specific
        "languages": None,                         # EUR-Lex languages
        "pages": None,                             # Number of pages (EUR-Lex)
        "latest_version": None,                    # EUR-Lex "Latest consolidated version"
        "url": None,                               # Document URL
        "topics": None,                            # Extracted from EEA result block
        "source": None,                            # Source name from EEA result block
        "is_new": None,                            # Boolean flag for new items on EEA website
        "scraped_at": datetime.now().isoformat()   # timestamp
    }

def save_metadata_to_file(metadata_dict, filename):
    """
    Used at the end of the `extract_metadata` functions that are in every scraper class (except the one of European Commission)
    Saves the metadata dictionary, that is made to follow the standard schema, to a JSON file. 
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, indent=4, ensure_ascii=False)
        logger.info(f"Metadata saved to {filename}")
    except Exception as e:
        logger.error(f"Failed to write metadata to {filename}: {e}")

