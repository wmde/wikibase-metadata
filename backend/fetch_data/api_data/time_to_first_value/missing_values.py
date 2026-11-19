"""Creation Logs Missing Values"""

from fetch_data.api_data.time_to_first_value.wikibase_creation_log_model import (
    WikibaseCreationLogRecord,
)


def missing_values(creation_logs: list[WikibaseCreationLogRecord]) -> bool:
    """Missing Values?"""

    if len(creation_logs) < 5:
        return True

    if creation_logs[0].title != "Item:Q50":
        return True

    for i in range(1, len(creation_logs)):
        if creation_logs[i].title != f"Item:Q{pow(10, i)}":
            print(creation_logs)
            return True

    return False
