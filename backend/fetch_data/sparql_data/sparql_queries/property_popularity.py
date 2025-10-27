"""Property Popularity"""

PROPERTY_POPULARITY_QUERY = """SELECT ?property (COUNT(*) AS ?propertyCount)
WHERE { ?item ?property ?object. }
GROUP BY ?property"""
