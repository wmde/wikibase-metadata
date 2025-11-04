import gql from 'graphql-tag'

const pageWikibasesQuery = gql`
	query PageWikibases(
		$pageNumber: Int!
		$pageSize: Int!
		$sortBy: WikibaseSortInput
		$wikibaseFilter: WikibaseFilterInput
	) {
		wikibaseList(
			pageNumber: $pageNumber
			pageSize: $pageSize
			sortBy: $sortBy
			wikibaseFilter: $wikibaseFilter
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

export default pageWikibasesQuery
