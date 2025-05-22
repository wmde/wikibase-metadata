"""Software Version Aggregation Fragment"""

SOFTWARE_VERSION_AGGREGATE_FRAGMENT = """
fragment WikibaseSoftwareVersionAggregateFragment
 on WikibaseSoftwareVersionAggregate {
  version
  versionDate
  versionHash
  wikibaseCount
}
"""


SOFTWARE_VERSION_DOUBLE_AGGREGATE_FRAGMENT = (
    """
fragment WikibaseSoftwareVersionDoubleAggregatePageFragment
 on WikibaseSoftwareVersionDoubleAggregatePage {
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
      ...WikibaseSoftwareVersionAggregateFragment
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
            ...WikibaseSoftwareVersionAggregateFragment
          }
        }
      }
    }
  }
}

"""
    + SOFTWARE_VERSION_AGGREGATE_FRAGMENT
)
