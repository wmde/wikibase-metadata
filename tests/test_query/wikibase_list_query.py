"""Test Wikibase List"""

WIKIBASE_LIST_QUERY = """
query PageWikibases($pageNumber: Int!, $pageSize: Int!, $sortBy: WikibaseSortInput, $wikibaseFilter: WikibaseFilterInput) {
  wikibaseList(
    pageNumber: $pageNumber
    pageSize: $pageSize
    sortBy: $sortBy
    wikibaseFilter: $wikibaseFilter
  ) {
    meta {
      pageNumber
      pageSize
      totalCount
      totalPages
    }
    data {
      ...WB
    }
  }
}

fragment WB on Wikibase {
  id
  title
  category
  description
  organization
  location {
    country
    region
  }
  languages {
    primary
    additional
  }
  urls {
    baseUrl
    actionApi
    articlePath
    indexApi
    scriptPath
    sparqlEndpointUrl
    sparqlFrontendUrl
    sparqlUrl
    specialStatisticsUrl
    specialVersionUrl
  }
  wikibaseType
  connectivityObservations {
    mostRecent {
      id
    }
  }
  externalIdentifierObservations {
    mostRecent {
      id
    }
  }
  logObservations {
    firstMonth {
      mostRecent {
        id
      }
    }
    lastMonth {
      mostRecent {
        id
      }
    }
  }
  propertyPopularityObservations {
    mostRecent {
      id
    }
  }
  quantityObservations {
    mostRecent {
      id
      totalTriples
    }
  }
  recentChangesObservations {
    mostRecent {
      id
      botChangeCount
      humanChangeCount
    }
  }
  softwareVersionObservations {
    mostRecent {
      id
    }
  }
  userObservations {
    mostRecent {
      id
    }
  }
}
"""
