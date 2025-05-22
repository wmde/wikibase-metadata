"""Software Version Observation Fragment"""

WIKIBASE_SOFTWARE_VERSION_FRAGMENT = """
fragment WikibaseSoftwareVersionFragment
 on WikibaseSoftwareVersion {
  id
  softwareName
  version
  versionDate
  versionHash
}
"""


WIKIBASE_SOFTWARE_VERSION_OBSERVATIONS_FRAGMENT = (
    """
fragment WikibaseSoftwareVersionObservationFragment
 on WikibaseSoftwareVersionObservation {
  id
  observationDate
  returnedData
  installedSoftware {
    ...WikibaseSoftwareVersionFragment
  }
}

"""
    + WIKIBASE_SOFTWARE_VERSION_FRAGMENT
)
