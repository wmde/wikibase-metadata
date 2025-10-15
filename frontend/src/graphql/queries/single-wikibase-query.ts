import gql from 'graphql-tag'

export const singleWikibaseQuery = gql`
	query SingleWikibase($wikibaseId: Int!) {
		wikibase(wikibaseId: $wikibaseId) {
			...SingleWikibase
		}
	}

	fragment SingleWikibase on Wikibase {
		id
		title
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
