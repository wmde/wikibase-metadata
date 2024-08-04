"""User Observation Fragment"""

WIKIBASE_USER_OBSERVATION_FRAGMENT = """
fragment WikibaseUserObservationStrawberryModelFragment on WikibaseUserObservationStrawberryModel {
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
