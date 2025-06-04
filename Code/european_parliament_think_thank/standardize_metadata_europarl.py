
from metadata_schema import get_standard_metadata_template

def standardize_metadata(metadata):

    """
    Converts raw metadata entries into a standardized schema format. 

    :param metadata: Dictionary where keys are document titles and values are dictionaries containing metadata
    :return: Dictionary with the same keys, but values mapped into a template structure with fields predefined in `metadata_schema.py`
    """

    standardized = {}
    for title, data in metadata.items():
        entry = get_standard_metadata_template()
        entry["id"] = title
        entry["title"] = data.get("title")
        entry["type"] = data.get("type")
        entry["author"] = ", ".join(data.get("authors", []))
        entry["date"] = data.get("date")
        entry["policy_area"] = data.get("policy_area")
        standardized[title] = entry
    return standardized