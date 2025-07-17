"""Count URL Properties"""

COUNT_URL_PROPERTIES_QUERY = str(
    "SELECT (COUNT(?urlProperty) as ?count) WHERE {"
    # get property entities that are of Url type
    "  ?urlProperty wikibase:propertyType wikibase:Url ."
    "}"
)
