import gql from 'graphql-tag'

const allTTFVWikibasesQuery = gql`
	query AllTTFVWikibases($wikibaseFilter: WikibaseFilterInput) {
		wikibaseList(pageNumber: 1, pageSize: -1, wikibaseFilter: $wikibaseFilter) {
			data {
				...WBTTFV
			}
		}
	}

	fragment WBTTFV on Wikibase {
		id
		title
		wikibaseType
		timeToFirstValueObservations {
			mostRecent {
				id
				initiationDate
				itemDates {
					id
					q
					creationDate
				}
			}
		}
	}
`

export default allTTFVWikibasesQuery
