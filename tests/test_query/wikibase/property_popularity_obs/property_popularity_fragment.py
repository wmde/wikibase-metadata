"""Property Popularity Observation Fragment"""

WIKIBASE_PROPERTY_POPULARITY_OBSERVATION_FRAGMENT = """
fragment WikibasePropertyPopularityObservationStrawberryModelFragment on WikibasePropertyPopularityObservationStrawberryModel {
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
