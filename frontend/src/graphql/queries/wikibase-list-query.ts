import gql from 'graphql-tag'

const listWikibasesQuery = gql`
	query ListWikibases {
		wikibaseList(
			pageNumber: 1
			pageSize: -1
			wikibaseFilter: { wikibaseType: { include: SUITE } }
		) {
			meta {
				totalCount
			}
			data {
				...WBItem
			}
		}
	}

	fragment WBItem on Wikibase {
		id
		title
		urls {
			baseUrl
			scriptPath
		}
	}
`

export default listWikibasesQuery
