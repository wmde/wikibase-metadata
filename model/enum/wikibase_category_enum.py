"""Wikibase Category Enum"""

import enum


class WikibaseCategory(enum.Enum):
    """Wikibase Category"""

    CULTURAL_AND_HISTORICAL = 1
    DIGITAL_COLLECTIONS_AND_ARCHIVES = 2
    EDUCATIONAL_AND_REFERENCE_COLLECTIONS = 3
    EXPERIMENTAL_AND_PROTOTYPE_PROJECTS = 4
    FICTIONAL_AND_CREATIVE_WORKS = 5
    LEGAL_AND_POLITICAL = 6
    LINGUISTIC_AND_LITERARY = 7
    MATHEMATICS_AND_SCIENCE = 8
    SEMANTIC_AND_PROSOPOGRAPHIC_DATA = 9
    SOCIAL_AND_ADVOCACY = 10
    TECHNOLOGY_AND_OPEN_SOURCE = 11


def wikibase_category_name(category: WikibaseCategory) -> str:
    """Human-Readable Category"""
    return category.name.replace("_", " ").title().replace("And", "and")
