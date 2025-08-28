"""Count External Identifier Statements"""

COUNT_EXTERNAL_IDENTIFIER_STATEMENTS_QUERY_WHERE = str(
    # get property entities that are external ids
    "?externalIdProperty wikibase:propertyType wikibase:ExternalId . "
    # get the matching direct property as it is used in statements
    "?externalIdProperty wikibase:directClaim ?directClaimProperty . "
    # get all statements using the direct property
    "?subject ?directClaimProperty ?value ."
)
