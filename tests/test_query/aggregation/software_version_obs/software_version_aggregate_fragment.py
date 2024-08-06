"""Software Version Aggregation Fragment"""

SOFTWARE_VERSION_AGGREGATE_FRAGMENT = """
fragment WikibaseSoftwareVersionAggregateStrawberryModelFragment
 on WikibaseSoftwareVersionAggregateStrawberryModel {
  version
  versionDate
  versionHash
  wikibaseCount
}
"""


SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT = (
    """
fragment WikibaseSoftwareVersionDoubleAggregateStrawberryModelPageFragment
 on WikibaseSoftwareVersionDoubleAggregateStrawberryModelPage {
  meta {
    pageNumber
    pageSize
    totalCount
    totalPages
  }
  data {
    softwareName
    wikibaseCount
    versions {
      ...WikibaseSoftwareVersionAggregateStrawberryModelFragment
    }
    majorVersions {
      version
      wikibaseCount
      minorVersions {
        version
        wikibaseCount
        patchVersions {
          version
          wikibaseCount
          subVersions {
            ...WikibaseSoftwareVersionAggregateStrawberryModelFragment
          }
        }
      }
    }
  }
}

"""
    + SOFTWARE_VERSION_AGGREGATE_FRAGMENT
)
