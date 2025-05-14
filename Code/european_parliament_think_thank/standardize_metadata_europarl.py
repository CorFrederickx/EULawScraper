
from metadata_schema import get_standard_metadata_template

def standardize_metadata(metadata):
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