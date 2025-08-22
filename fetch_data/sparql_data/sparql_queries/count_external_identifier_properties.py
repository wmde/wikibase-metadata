"""Count External Identifier Properties"""

COUNT_EXTERNAL_IDENTIFIER_PROPERTIES_QUERY_WHERE = str(
    # get property entities that are external ids
    "?externalIdProperty wikibase:propertyType wikibase:ExternalId ."
)
