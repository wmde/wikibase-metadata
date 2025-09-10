"""External Identifier Observation Fragment"""

WIKIBASE_EXTERNAL_IDENTIFIER_OBSERVATION_FRAGMENT = """
fragment WikibaseExternalIdentifierObservationFragment on WikibaseExternalIdentifierObservation {
  id
  observationDate
  returnedData
  totalItems
  totalLexemes
  totalProperties
  totalTriples
  totalExternalIdentifierProperties
  totalExternalIdentifierStatements
  totalUrlProperties
  totalUrlStatements
}
"""
