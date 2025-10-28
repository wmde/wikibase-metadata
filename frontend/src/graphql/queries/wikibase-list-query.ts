import gql from 'graphql-tag'

export const pageWikibasesQuery = gql`
	query PageWikibases($pageNumber: Int!, $pageSize: Int!, $wikibaseFilter: WikibaseFilterInput) {
		wikibaseList(wikibaseFilter: $wikibaseFilter, pageNumber: $pageNumber, pageSize: $pageSize) {
			meta {
				totalCount
			}
			data {
				...WB
			}
		}
	}

	fragment WB on Wikibase {
		id
		title
		urls {
			baseUrl
		}
		wikibaseType
		quantityObservations {
			mostRecent {
				totalTriples
			}
		}
		recentChangesObservations {
			mostRecent {
				botChangeCount
				humanChangeCount
			}
		}
	}
`
