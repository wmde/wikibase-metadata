"""Log Observation Fragment"""

WIKIBASE_LOG_OBSERVATION_FRAGMENT = """
fragment WikibaseLogMonthFragment on WikibaseLogMonth {
  id
  observationDate
  returnedData
  logCount
  allUsers
  humanUsers
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
