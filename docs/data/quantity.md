### Quantity Observations:

There are two kinds of quantity observations; one made using SPARQL queries, and one made using API calls.

#### API Quantity

We query the wikibase's action api (`/[scriptPath]/api.php`) for the namespaces data, to identify the namespaces for items, properties, and lexemes (if present).

For each of those retrieved, we query the `allpages` endpoint for all pages within the namespace, and save the number of unique page titles.

#### SPARQL Quantity

Using SPARQL, we query for the total number of items, lexemes, and properties in the data.

- Total Items
- Total Lexemes
- Total Properties
- Total Triples

##### Example:

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
