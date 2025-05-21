from metadata_schema import get_standard_metadata_template

def standardize_metadata(metadata):

    standardized = {}
    for doc_id, data in metadata.items():
        entry = get_standard_metadata_template()

        entry["id"] = doc_id
        entry["title"] = data.get("Title")
        entry["url"] = data.get("Source URL")
        entry["date"] = data.get("Date")
        entry["topics"] = data.get("Topics")
        entry["source"] = data.get("Source")
        entry["is_new"] = data.get("Is New")

        standardized[doc_id] = entry

    return standardized