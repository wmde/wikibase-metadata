import gql from 'graphql-tag'

export const pageWikibasesQuery = gql`
	query PageWikibases(
		$pageNumber: Int!
		$pageSize: Int!
		$wikibaseFilter: WikibaseFilterInput
		$sortBy: WikibaseSortInput
	) {
		wikibaseList(
			wikibaseFilter: $wikibaseFilter
			pageNumber: $pageNumber
			pageSize: $pageSize
			sortBy: $sortBy
		) {
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
		category
		description
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
