### Time to First Value Observations:

This data is fetched from the Action API. We return the date of the first log in the wiki, and the date of the first revision (deleted or not) of items Q1, Q10, Q100, etc. If we can't find Q1, we'll check Q2, Q3, up to Q6. The intention is to see a rough time scale for adding data to the wikibase - does a wiki get to Q100 in an hour? A week? A year?

#### Example:

Query:

```graphql
query MyQuery($wikibaseId: Int!) {
	wikibase(wikibaseId: $wikibaseId) {
		id
		timeToFirstValueObservations {
			mostRecent {
				...WikibaseTimeToFirstValueObservationFragment
			}
			allObservations {
				...WikibaseTimeToFirstValueObservationFragment
			}
		}
	}
}

fragment WikibaseTimeToFirstValueObservationFragment on WikibaseTimeToFirstValueObservation {
	id
	observationDate
	returnedData
	initiationDate
	itemDates {
		id
		q
		creationDate
	}
}
```

Result:

```json
{
  "data": {
    "wikibase": {
      "id": "14",
      "timeToFirstValueObservations": {
        "mostRecent": {
          "id": "1",
          "observationDate": "2025-08-27T13:42:17.654426",
          "returnedData": true,
          "initiationDate": "2020-08-15T17:33:47",
          "itemDates": [
            {
              "id": "1",
              "q": 1,
              "creationDate": "2020-08-31T14:13:58"
            },
            {
              "id": "2",
              "q": 10,
              "creationDate": "2020-08-31T21:47:28"
            },
            {
              "id": "3",
              "q": 100,
              "creationDate": "2020-08-31T21:48:36"
            },
			...
          ]
        },
        "allObservations": [
          {
            "id": "1",
            "observationDate": "2025-08-27T13:42:17.654426",
			...
          }
        ]
      }
    }
  }
}
```

Data abbreviated for brevity.
