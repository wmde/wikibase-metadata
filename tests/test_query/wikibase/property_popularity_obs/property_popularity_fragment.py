"""Property Popularity Observation Fragment"""

WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT = """
fragment WikibasePropertyPopularityObservationStrawberryModelFragment on WikibasePropertyPopularityObservationStrawberryModel {
  id
  observationDate
  returnedData
  propertyPopularityCounts(pageNumber: 1, pageSize: 10) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      id
      propertyUrl
      usageCount
    }
  }
}
"""
