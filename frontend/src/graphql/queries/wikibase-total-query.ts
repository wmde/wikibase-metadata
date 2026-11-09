import gql from 'graphql-tag'

const totalWikibasesQuery = gql`
	query TotalWikibases {
		wikibaseList(pageNumber: 1, pageSize: -1) {
			meta {
				totalCount
			}
		}
		aggregateQuantity {
			totalTriples
		}
		aggregateRecentChanges {
			botChangeCount
			humanChangeCount
		}
	}
`

export default totalWikibasesQuery
