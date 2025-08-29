"""Count External Identifier Properties"""

# get property entities that are external ids
COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY_WHERE = str(
    "?externalIdProperty wikibase:propertyType wikibase:ExternalId .",
)
