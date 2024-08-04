"""User Observation Fragment"""

WIKIBASE_SOFTWARE_VERSION_FRAGMENT = """
fragment WikibaseSoftwareVersionStrawberryModelFragment on WikibaseSoftwareVersionStrawberryModel {
  id
  softwareName
  version
  versionDate
  versionHash
}
"""


WIKIBASE_SOFTWARE_VERSION_OBSERVATIONS_FRAGMENT = (
    """
fragment WikibaseSoftwareVersionObservationStrawberryModelFragment on WikibaseSoftwareVersionObservationStrawberryModel {
  id
  observationDate
  returnedData
  installedSoftware {
    ...WikibaseSoftwareVersionStrawberryModelFragment
  }
}

"""
    + WIKIBASE_SOFTWARE_VERSION_FRAGMENT
)
