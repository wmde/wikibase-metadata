"""Connectivity Observation Fragment"""

WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT = """
fragment WikibaseConnectivityObservationFragment on WikibaseConnectivityObservation {
  id
  observationDate
  returnedData
  returnedLinks
  totalConnections
  averageConnectedDistance
  connectivity
  relationshipItemCounts {
    id
    relationshipCount
    itemCount
  }
  relationshipObjectCounts {
    id
    relationshipCount
    objectCount
  }
}
"""
