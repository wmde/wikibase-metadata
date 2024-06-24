"""Item Property Counts"""

ITEM_PROPERTY_COUNTS_QUERY = """SELECT ?relationshipCount (COUNT(*) AS ?itemCount) WHERE {
  SELECT ?item (COUNT(*) AS ?relationshipCount) WHERE {
    ?item ?property ?object;
      wikibase:sitelinks [].
    ?object wikibase:sitelinks [].
  }
  GROUP BY ?item
}
GROUP BY ?relationshipCount
ORDER BY ?relationshipCount"""
