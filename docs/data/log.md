### Log Observations:

Using the Action API, we query separately for the first month of logs and the last 30 days'. We update the first month annually and the last month approximately monthly.

We calculate the following:

- `logCount`: Number of logs in range (if any)
- Date of first and last logs in range (if any); user type (bot or human) of the last log
- number of users with at least 1 (`allUsers`) and at least 5 (`activeUsers`) records in the logs
- number of users we think are human with at least 1 (`humanUsers`) and at least 5 (`activeHumanUsers`) records in the logs
- We categorize the logs into types and save similar information broken out by log type. There are currently 76 log types, plus an UNCLASSIFIED catch-all, ranging from ITEM_CREATE to ACHIEVEMENT_BADGE
- We categorize the users into BOT, MISSING, HUMAN, or NONE, and save similar information broken out by user type

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 10) {
		logObservations {
			firstMonth {
				mostRecent {
					...WikibaseLogMonthFragment
				}
			}
			lastMonth {
				mostRecent {
					...WikibaseLogMonthFragment
				}
			}
		}
	}
}

fragment WikibaseLogMonthFragment on WikibaseLogMonth {
	id
	observationDate
	returnedData
	firstLog {
		date
	}
	lastLog {
		date
		userType
	}
	logCount
	allUsers
	activeUsers
	humanUsers
	activeHumanUsers
	logTypeRecords {
		id
		logType
		logCount
		firstLogDate
		lastLogDate
		allUsers
		activeUsers
		humanUsers
		activeHumanUsers
	}
	userTypeRecords {
		id
		userType
		logCount
		firstLogDate
		lastLogDate
		allUsers
		activeUsers
	}
}
```

Result:

```json
{
  "data": {
    "wikibase": {
      "logObservations": {
        "firstMonth": {
          "mostRecent": {
            "id": "229",
            "observationDate": "2024-08-08T11:29:46",
            "returnedData": true,
            "firstLog": {
              "date": "2021-03-19T09:20:21"
            },
            "lastLog": {
              "date": "2021-04-13T15:07:57",
              "userType": null
            },
            "logCount": 12,
            "allUsers": 4,
            "activeUsers": null,
            "humanUsers": 3,
            "activeHumanUsers": null,
            "logTypeRecords": [
			  ...
              {
                "id": "600",
                "logType": "ITEM_CREATE",
                "logCount": 1,
                "firstLogDate": "2021-03-20T10:36:45",
                "lastLogDate": "2021-03-20T10:36:45",
                "allUsers": 1,
                "activeUsers": 0,
                "humanUsers": 0,
                "activeHumanUsers": 0
              },
              {
                "id": "601",
                "logType": "PROPERTY_CREATE",
                "logCount": 5,
                "firstLogDate": "2021-03-22T19:56:32",
                "lastLogDate": "2021-04-13T15:07:57",
                "allUsers": 1,
                "activeUsers": 1,
                "humanUsers": 0,
                "activeHumanUsers": 0
              },
              {
                "id": "602",
                "logType": "USER_CREATE",
                "logCount": 4,
                "firstLogDate": "2021-03-19T09:20:21",
                "lastLogDate": "2021-03-24T08:35:41",
                "allUsers": 3,
                "activeUsers": 0,
                "humanUsers": 3,
                "activeHumanUsers": 0
              }
            ],
            "userTypeRecords": [
              {
                "id": "152",
                "userType": "BOT",
                "logCount": 6,
                "firstLogDate": "2021-03-20T10:36:45",
                "lastLogDate": "2021-04-13T15:07:57",
                "allUsers": 1,
                "activeUsers": 1
              },
              {
                "id": "153",
                "userType": "USER",
                "logCount": 6,
                "firstLogDate": "2021-03-19T09:20:21",
                "lastLogDate": "2021-04-07T11:37:37",
                "allUsers": 3,
                "activeUsers": 0
              }
            ]
          }
        },
        "lastMonth": {
          "mostRecent": {
            "id": "230",
            "observationDate": "2024-08-08T11:29:46",
            "returnedData": true,
            "firstLog": {
              "date": "2024-07-09T11:20:15"
            },
            "lastLog": {
              "date": "2024-07-26T11:30:36",
              "userType": "BOT"
            },
            "logCount": 81,
            "allUsers": 1,
            "activeUsers": 1,
            "humanUsers": 0,
            "activeHumanUsers": 0,
            "logTypeRecords": [
              {
                "id": "603",
                "logType": "ITEM_CREATE",
                "logCount": 81,
                "firstLogDate": "2024-07-09T11:20:15",
                "lastLogDate": "2024-07-26T11:30:36",
                "allUsers": 1,
                "activeUsers": 1,
                "humanUsers": 0,
                "activeHumanUsers": 0
              }
            ],
            "userTypeRecords": [
              {
                "id": "154",
                "userType": "BOT",
                "logCount": 81,
                "firstLogDate": "2024-07-09T11:20:15",
                "lastLogDate": "2024-07-26T11:30:36",
                "allUsers": 1,
                "activeUsers": 1
              }
            ]
          }
        }
      }
    }
  }
}
```
