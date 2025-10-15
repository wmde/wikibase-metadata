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
			sparqlFrontendUrl
		}
		wikibaseType
		quantityObservations {
			mostRecent {
				observationDate
				totalItems
				totalLexemes
				totalProperties
				totalTriples
			}
		}
		recentChangesObservations {
			mostRecent {
				observationDate
				botChangeCount
				humanChangeCount
			}
		}
		timeToFirstValueObservations {
			mostRecent {
				observationDate
				initiationDate
			}
		}
	}
`
