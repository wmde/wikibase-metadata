"""Wikibase Software Version Table"""

import enum


class WikibaseSoftwareTypes(enum.Enum):
    """Wikibase Software Types"""

    SOFTWARE = 1
    SKIN = 2
    EXTENSION = 3
    LIBRARY = 4
