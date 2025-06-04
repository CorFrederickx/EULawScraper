
from metadata_schema import get_standard_metadata_template

def standardize_metadata(metadata):

    """
    Converts raw metadata entries into a standardized schema format. 

    :param metadata: Dictionary where keys are document titles and values are dictionaries containing metadata
    :return: Dictionary with the same keys, but values mapped into a template structure with fields predefined in `metadata_schema.py`
    """
    
    standardized = {}
    for doc_id, data in metadata.items():
        entry = get_standard_metadata_template()
        entry["id"] = doc_id
        entry["form"] = data.get("Form")
        entry["author"] = data.get("Author")
        entry["date"] = data.get("Date of document")
        entry["status"] = data.get("In force")
        entry["languages"] = data.get("Languages")
        entry["pages"] = data.get("Number of pages")
        entry["latest_version"] = data.get("Latest consolidated version")
        entry["url"] = data.get("url")
        standardized[doc_id] = entry
    return standardized




