import gql from 'graphql-tag'

export const pageWikibasesQuery = gql`
  query pageWikibases($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
    wikibaseList(wikibaseFilter: $wikibaseFilter, pageNumber: $pageNumber, pageSize: $pageSize) {
      meta {
        totalCount
      }
      data {
        id
        urls {
          baseUrl
        }
        wikibaseType
      }
    }
  }
`
