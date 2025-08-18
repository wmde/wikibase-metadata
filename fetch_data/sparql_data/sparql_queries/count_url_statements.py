"""Count URL Statements"""

COUNT_URL_STATEMENTS_QUERY = str(
    "SELECT (COUNT(?value) as ?count) WHERE {"
    # get property entities that are of Url type
    "  ?urlProperty wikibase:propertyType wikibase:Url ."
    # get the matching direct property as it is used in statements
    "  ?urlProperty wikibase:directClaim ?directClaimProperty ."
    # get all statements using the direct property
    "  ?subject ?directClaimProperty ?value ."
    "}"
)
