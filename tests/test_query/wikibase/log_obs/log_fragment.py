"""Log Observation Fragment"""

WIKIBASE_LOG_OBSERVATION_FRAGMENT = """
fragment WikibaseLogMonthFragment on WikibaseLogMonth {
  id
  observationDate
  returnedData
  logCount
  allUsers
  activeUsers
  humanUsers
  activeHumanUsers
  firstLog {
    date
  }
  lastLog {
    date
    userType
  }
  logTypeRecords {
    id
    logType
    firstLogDate
    lastLogDate
    logCount
    allUsers
    activeUsers
    humanUsers
    activeHumanUsers
  }
  userTypeRecords {
    id
    userType
    firstLogDate
    lastLogDate
    logCount
    allUsers
    activeUsers
  }
}
"""
