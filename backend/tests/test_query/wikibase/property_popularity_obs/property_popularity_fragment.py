"""Property Popularity Observation Fragment"""

WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT = """
fragment WikibasePropertyPopularityObservationFragment on WikibasePropertyPopularityObservation {
  id
  observationDate
  returnedData
  propertyPopularityCounts {
    id
    propertyUrl
    usageCount
  }
}
"""
