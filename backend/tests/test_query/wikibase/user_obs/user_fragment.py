"""User Observation Fragment"""

WIKIBASE_USER_OBSERVATION_FRAGMENT = """
fragment WikibaseUserObservationFragment on WikibaseUserObservation {
  id
  observationDate
  returnedData
  totalUsers
  userGroups {
    id
    group {
      id
      groupName
      wikibaseDefault
    }
    groupImplicit
    userCount
  }
}
"""
