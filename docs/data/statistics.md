### Statistics Observations:

This data is parsed from the Wikibase's Special:Statistics page. The following fields are fetched:

- Page Statistics:
  - Content Pages
  - Pages
  - Uploaded Files
- Edit Statistics:
  - Page Edits
- User Statistics:
  - Registered Users
  - Active Users
  - Administrators
- Other Statistics:
  - Words in Content Pages

Some Wikibases remain on MediaWiki versions that do not include all of these statistics; we return null for each statistics that cannot be located.

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 1) {
		id
		statisticsObservations {
			mostRecent {
				id
				observationDate
				returnedData
				edits {
					editsPerPageAvg
					totalEdits
				}
				files {
					totalFiles
				}
				pages {
					contentPageWordCountAvg
					contentPageWordCountTotal
					contentPages
					totalPages
				}
				users {
					activeUsers
					totalAdmin
					totalUsers
				}
			}
		}
	}
}
```

`editsPerPageAvg` and `contentPageWordCountAvg` are calculated at query time.

Result:

```json
{
	"data": {
		"wikibase": {
			"id": "1",
			"statisticsObservations": {
				"mostRecent": {
					"id": "96",
					"observationDate": "2024-08-21T19:29:12",
					"returnedData": true,
					"edits": {
						"editsPerPageAvg": 2.8565157050360703,
						"totalEdits": 36150983
					},
					"files": {
						"totalFiles": 30
					},
					"pages": {
						"contentPageWordCountAvg": 0.032581015189210576,
						"contentPageWordCountTotal": 27750,
						"contentPages": 851723,
						"totalPages": 12655622
					},
					"users": {
						"activeUsers": 5,
						"totalAdmin": 17,
						"totalUsers": 465
					}
				}
			}
		}
	}
}
```
