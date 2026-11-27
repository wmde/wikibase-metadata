### Quantity Observations:

Using SPARQL, we query for the total number of items, lexemes, and properties in the data.

- Total Items
- Total Lexemes
- Total Properties
- Total Triples

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 43) {
		id
		quantityObservations {
			mostRecent {
				id
				observationDate
				returnedData
				totalItems
				totalLexemes
				totalProperties
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
			"quantityObservations": {
				"mostRecent": {
					"id": "76",
					"observationDate": "2024-06-24T08:58:24",
					"returnedData": true,
					"totalItems": 86,
					"totalLexemes": 0,
					"totalProperties": 48
				}
			}
		}
	}
}
```

Data abbreviated for brevity.
