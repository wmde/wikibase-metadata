"""Quantity Observation Fragment"""

WIKIBASE_QUANTITY_OBSERVATION_FRAGMENT = """
fragment WikibaseQuantityObservationFragment on WikibaseQuantityObservation {
  id
  observationDate
  returnedData
  totalItems
  totalLexemes
  totalProperties
  totalTriples
}
"""
