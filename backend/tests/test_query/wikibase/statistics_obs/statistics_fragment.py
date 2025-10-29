"""Statistics Observation Fragment"""

WIKIBASE_STATISTICS_OBSERVATION_FRAGMENT = """
fragment WikibaseStatisticsObservationFragment on WikibaseStatisticsObservation {
  id
  observationDate
  returnedData
  edits {
    editsPerPageAvg
    totalEdits
  }
  files {
    totalFiles
  }
  pages {
    contentPages
    contentPageWordCountAvg
    contentPageWordCountTotal
    totalPages
  }
  users {
    activeUsers
    totalAdmin
    totalUsers
  }
}
"""
