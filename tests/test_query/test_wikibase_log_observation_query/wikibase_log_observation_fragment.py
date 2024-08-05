"""Log Observation Fragment"""

WIKIBASE_LOG_OBSERVATION_FRAGMENT = """
fragment WikibaseLogObservationStrawberryModelFragment on WikibaseLogObservationStrawberryModel {
  id
  observationDate
  returnedData
  instanceAge
  firstLog {
    date
  }
  firstMonth {
    ...WikibaseLogMonthStrawberryModelFragment
  }
  lastLog {
    date
    userType
  }
  lastMonth {
    ...WikibaseLogMonthStrawberryModelFragment
  }
}

fragment WikibaseLogMonthStrawberryModelFragment on WikibaseLogMonthStrawberryModel {
  id
  firstLogDate
  lastLogDate
  logCount
  allUsers
  humanUsers
  logTypeRecords {
    id
    logType
    firstLogDate
    lastLogDate
    logCount
    allUsers
    humanUsers
  }
  userTypeRecords {
    id
    userType
    firstLogDate
    lastLogDate
    logCount
    allUsers
  }
}
"""
