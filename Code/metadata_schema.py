
# a function to store all according to a unified schema

from datetime import datetime
import json

def get_standard_metadata_template():
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
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(metadata_dict, f, indent=4, ensure_ascii=False)
        print(f"Metadata saved to {filename}")
    except Exception as e:
        print(f"Failed to write metadata to {filename}: {e}")
