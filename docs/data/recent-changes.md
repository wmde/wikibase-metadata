### Recent Changes:

Get the list of recent changes from a Wikibase instance. The [Recent Changes MediaWiki API is documented here](https://www.mediawiki.org/wiki/API:RecentChanges). A Recent Changes Observation is always calculated for the past 30 days. All change types are included; which are: `edit`, `new`, `log` and `categorize`. An Observation contains the following fields:

| Field | Description |
| --- | --- |
| `human_change_count` | Number of changes made by humans as reported by the MediaWiki Recent Changes API when called with the `!bot` flag. |
| `human_change_user_count` | Number of unique users found in changes requested with `!bot` flag, derived from all usernames, IP addresses for anonymous edits as well as userid in the "userhidden case". |
| `human_change_active_user_count` | Number of unique users with at least 5 records found in changes requested with `!bot` flag, derived from all usernames, IP addresses for anonymous edits as well as userid in the "userhidden case". |
| `bot_change_count` | Number of changes made by bots as reported by the MediaWiki Recent Changes API when called with the `bot` flag. |
| `bot_change_user_count` | Number of unique bots found in changes requested with `bot` flag, derived from all bot/usernames. |
| `bot_change_active_user_count` | Number of unique bots with at least 5 records found in changes requested with `bot` flag, derived from all bot/usernames. |
| `first_change_date` | Date of first change, no matter if it was made by a human or bot. |
| `last_change_date` | Date of last change, no matter if it was made by a human or bot. |

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 1) {
		id
		recentChangesObservations {
			mostRecent {
				observationDate
				humanChangeCount
				humanChangeUserCount
				humanChangeActiveUserCount
				botChangeCount
				botChangeUserCount
				botChangeActiveUserCount
				firstChangeDate
				lastChangeDate
				returnedData
			}
		}
	}
}
```

Result:

```json
{
	"data": {
		"wikibase": {
			"id": "1",
			"recentChangesObservations": {
				"mostRecent": {
					"observationDate": "2025-07-29T13:36:00",
					"humanChangeCount": 2302,
					"humanChangeUserCount": 1,
					"humanChangeActiveUserCount": 1,
					"botChangeCount": 4,
					"botChangeUserCount": 1,
					"botChangeActiveUserCount": 1,
					"firstChangeDate": "2025-07-03T08:31:51",
					"lastChangeDate": "2025-07-25T15:41:47",
					"returnedData": true
				}
			}
		}
	}
}
```
