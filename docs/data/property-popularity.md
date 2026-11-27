### Property Popularity Observations:

Using SPARQL, we query for all properties in the Wikibase, and the number of times they are used in the data. We return that list.

- Property URL: the format the properties are returned in, as many are not specific to this particular wikibase
- Usage Count: Number of times the property is used

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 43) {
		id
		propertyPopularityObservations {
			mostRecent {
				id
				observationDate
				returnedData
				propertyPopularityCounts {
					id
					propertyUrl
					usageCount
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
      "propertyPopularityObservations": {
        "mostRecent": {
          "id": "1",
          "observationDate": "2024-06-24T13:05:05",
          "returnedData": true,
          "propertyPopularityCounts": [
            {
              "id": "110",
              "propertyUrl": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
              "usageCount": 936
            },
            {
              "id": "1",
              "propertyUrl": "http://wikiba.se/ontology#rank",
              "usageCount": 323
            },
            ...
            {
              "id": "112",
              "propertyUrl": "http://schema.org/dateModified",
              "usageCount": 135
            },
            ...
            {
              "id": "31",
              "propertyUrl": "http://modelling.dissco.tech/prop/P15",
              "usageCount": 1
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
