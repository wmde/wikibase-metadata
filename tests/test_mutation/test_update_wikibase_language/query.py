"""Wikibase Languages Query"""

WIKIBASE_LANGUAGES_QUERY = """
query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    languages {
      primary
      additional
    }
  }
}"""
