"""Count Lexemes"""

COUNT_LEXEMES_QUERY = """
PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>

SELECT (COUNT(*) AS ?count) WHERE { ?l rdf:type ontolex:LexicalEntry. }
"""
