
# a function to store all according to a unified schema

from datetime import datetime

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
        "scraped_at": datetime.now().isoformat()   # timestamp
    }




