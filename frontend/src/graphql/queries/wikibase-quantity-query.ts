import gql from 'graphql-tag'

const allQuantityWikibasesQuery = gql`
	query AllQuantityWikibases($wikibaseFilter: WikibaseFilterInput) {
		wikibaseList(pageNumber: 1, pageSize: -1, wikibaseFilter: $wikibaseFilter) {
			data {
				...WBQuantity
			}
		}
	}

	fragment WBQuantity on Wikibase {
		id
		title
		wikibaseType
		quantityObservations {
			allObservations {
				id
				observationDate
				returnedData
				totalItems
				totalLexemes
				totalProperties
				totalTriples
			}
		}
	}
`

export default allQuantityWikibasesQuery
