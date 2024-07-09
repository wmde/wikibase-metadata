"""Count Triples"""

COUNT_TRIPLES_QUERY = (
    """SELECT (COUNT(*) AS ?count) WHERE { ?item ?property ?object. }"""
)
