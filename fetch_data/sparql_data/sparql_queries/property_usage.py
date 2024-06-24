"""Property Usage"""

PROPERTY_USAGE_QUERY = """SELECT ?property (COUNT(*) AS ?propertyCount) WHERE { ?item ?property ?object. }
GROUP BY ?property"""
