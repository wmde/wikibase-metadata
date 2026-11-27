### User Observations:

This data is fetched from the Action API. We return the total number of users registered in the Wikibase, and for each group, we save the following data:

- Group Name
- Wikibase Default: Whether or not the group is part of the default list from a stock Wikibase install
- Group Implicit: Whether the group is implicitly applied to users
- User Count

_We do not save the names of any users in the database._

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 43) {
		id
		userObservations {
			mostRecent {
				id
				observationDate
				returnedData
				totalUsers
				userGroups {
					id
					group {
						id
						groupName
						wikibaseDefault
					}
					groupImplicit
					userCount
				}
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
      "id": "43",
      "userObservations": {
        "mostRecent": {
          "id": "43",
          "observationDate": "2024-06-17T13:41:14.013073",
          "returnedData": true,
          "totalUsers": 22,
          "userGroups": [
            {
              "id": "312",
              "group": {
                "id": "1",
                "groupName": "*",
                "wikibaseDefault": true
              },
              "groupImplicit": true,
              "userCount": 22
            },
            ...
            {
              "id": "316",
              "group": {
                "id": "5",
                "groupName": "bureaucrat",
                "wikibaseDefault": true
              },
              "groupImplicit": false,
              "userCount": 2
            },
            ...
          ]
        }
      }
    }
  }
}
```

Data abbreviated for brevity.
