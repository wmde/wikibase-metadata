"""Count Properties"""

COUNT_PROPERTIES_QUERY = """SELECT (COUNT(*) AS ?count) WHERE {
  ?property a wikibase:Property.
}"""
