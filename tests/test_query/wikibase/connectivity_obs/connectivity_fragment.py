"""Connectivity Observation Fragment"""

WIKIBASE_CONNECTIVITY_OBSERVATION_FRAGMENT = """
fragment WikibaseConnectivityObservationStrawberryModelFragment on WikibaseConnectivityObservationStrawberryModel {
  id
  observationDate
  returnedData
  returnedLinks
  totalConnections
  averageConnectedDistance
  connectivity
  relationshipItemCounts(pageNumber: 1, pageSize: 10) {
    meta {
      ...PageMetadataFragment
    }
    data {
      id
      relationshipCount
      itemCount
    }
  }
  relationshipObjectCounts(pageNumber: 1, pageSize: 10) {
    meta {
      ...PageMetadataFragment
    }
    data {
      id
      relationshipCount
      objectCount
    }
  }
}

fragment PageMetadataFragment on PageMetadata {
  pageNumber
  pageSize
  totalCount
  totalPages
}
"""
