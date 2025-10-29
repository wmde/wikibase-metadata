"""Count Items"""

COUNT_ITEMS_QUERY = """SELECT (COUNT(*) AS ?count) WHERE {
  ?item wikibase:sitelinks [].
}"""
