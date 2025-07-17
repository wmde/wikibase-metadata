"""Count External Identifier Properties"""

COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY = str(
    "SELECT (COUNT(?externalIdProperty) as ?count) WHERE {"
    # get property entities that are external ids
    "  ?externalIdProperty wikibase:propertyType wikibase:ExternalId ."
    "}"
)
