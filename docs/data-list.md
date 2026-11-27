# Data Metrics

## Individual Wikibase Instances:

### Manually Added Attributes:

- Title
- Organization
- Languages
  - Primary Language
  - Additional Languages
- Location
  - Country
  - Region
- URLs:
  - Base URL
  - Action API URL
  - Index API URL
  - SPARQL Endpoint URL (machine endpoint)
  - SPARQL UI URL (human-usable UI)
  - Special:Version URL

#### Example:

Query:

```graphql
query MyQuery {
	wikibase(wikibaseId: 10) {
		id
		title
		organization
		languages {
			primary
			additional
		}
		location {
			country
			region
		}
		urls {
			baseUrl
			actionApi
			indexApi
			sparqlEndpointUrl
			sparqlUrl
			specialVersionUrl
		}
	}
}
```

Results:

```json
{
	"data": {
		"wikibase": {
			"id": "10",
			"title": "ELTEdata",
			"organization": "Digital Humanities Department of ELTE BTK (Eötvös Loránd University Faculty of Humanities)",
			"languages": {
				"primary": "Korean",
				"additional": ["English", "German", "Japanese", "Spanish"]
			},
			"location": {
				"country": "Hungary",
				"region": "Europe"
			},
			"urls": {
				"baseUrl": "https://eltedata.elte-dh.hu",
				"actionApi": "https://eltedata.elte-dh.hu/w/api.php",
				"indexApi": "https://eltedata.elte-dh.hu/w/index.php",
				"sparqlEndpointUrl": "https://query.elte-dh.hu/proxy/wdqs/bigdata/namespace/wdq/sparql",
				"sparqlUrl": "https://query.elte-dh.hu/",
				"specialVersionUrl": "https://eltedata.elte-dh.hu/wiki/Special:Version"
			}
		}
	}
}
```

### Observations:

All observations return `observationDate`, the date the observation was attempted, and `returnedData`, a boolean to signify if the observation attempt was successful. All data fields are null if `returnedData` is false.

For each type of observation, the most recent successful observation -- maximum `observationDate` where `returnedData == True` -- is returned as `mostRecent`, and all observations, successful or not, are returned in a collection labelled `allObservations`. `mostRecent` will be `null` if there are no successful observations.

The relationship between `mostRecent` and `allObservations` is demonstrated in Connectivity Observations, but omitted elsewhere for brevity.

The list of observations, with additional details and example queries:

- [Connectivity](data/connectivity.md)
- [Log](data/log.md)
- [Property Popularity](data/property-popularity.md)
- [Quantity](data/quantity.md)
- [Recent Changes](data/recent-changes.md)
- [Statistics](data/statistics.md)
- [Software Version](data/software-version.md)
- [Time to First Value](data/time-to-first-value.md)
- [User Groups](data/user.md)

## Paginated Wikibase List:

A paginated list of the Wikibase instances.

Arguments:

- Page Number: 1-indexed page number
- Page Size: number of Wikibases per page

Results:

- Meta:
  - Page Number: same as the input
  - Page Size: same as the input
  - Total Count: total number of Wikibases
  - Total Pages: total number of pages, with the given total and page size
- Data: list of Wikibases, ordered by id ascending. Every field noted above in Individual Wikibase Instances is accessible here.

#### Example:

Query:

```graphql
query MyQuery {
	wikibaseList(pageNumber: 2, pageSize: 10) {
		meta {
			pageNumber
			pageSize
			totalCount
			totalPages
		}
		data {
			id
			title
			urls {
				baseUrl
			}
			quantityObservations {
				mostRecent {
					totalItems
					totalLexemes
					totalProperties
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
    "wikibaseList": {
      "meta": {
        "pageNumber": 2,
        "pageSize": 10,
        "totalCount": 43,
        "totalPages": 5
      },
      "data": [
        {
          "id": "11",
          "title": "Kunstmuseum API",
          "urls": {
            "baseUrl": "https://api.kunstmuseum.nl"
          },
          "quantityObservations": {
            "mostRecent": {
              "totalItems": 37267,
              "totalLexemes": 0,
              "totalProperties": 113
            }
          }
        },
        ...
        {
          "id": "20",
          "title": "Safer Nicotine Wiki",
          "urls": {
            "baseUrl": "https://safernicotine.wiki/mediawiki"
          },
          "quantityObservations": {
            "mostRecent": null
          }
        }
      ]
    }
  }
}
```

Data abbreviated for brevity.

## Aggregated Data:

Data aggregated from the `mostRecent` record for each Wikibase.

### Aggregated Created

This aggregates the number of wikibases created by year. The creation date is derived from the first log date of each wikibase,.

#### Example:

Query:

```graphql
query MyQuery {
	aggregateCreated {
		wikibaseCount
		year
	}
}
```

Result:

```json
{
  "data": {
    "aggregateCreated": [
      {
        "wikibaseCount": 1,
        "year": 2005
      },
      {
        "wikibaseCount": 1,
        "year": 2006
      },
      {
        "wikibaseCount": 1,
        "year": 2011
      },
      ...
    ]
  }
}
```

Data abbreviated for brevity.

### Aggregated Extension/Library/Skin/Software Popularity:

All four work exactly the same way, so they are outlined together here.

Aggregated from the Software Version Observations above. The data is paginated as above in Wikibase List; the Page Number and Page Size arguments are the same, and the queries return Meta and Data as above.

- Software Name
- Wikibase Count: Number of Wikibases in which software is installed
- Versions: List of versions, ordered by wikibase count descending
  - Version: Version string (if existant)
  - Version Date: Version date (if existant)
  - Version Hash: Version commit hash (if existant)
  - Wikibase Count: Number of Wikibases with this specific version
  - If a version is parsable as a SemVer version, then we have a major/minor/patch version tree

#### Example:

Query:

```graphql
query MyQuery {
	aggregateSoftwarePopularity(pageSize: 10, pageNumber: 1) {
		meta {
			totalCount
		}
		data {
			softwareName
			wikibaseCount
			versions {
				version
				versionDate
				versionHash
				wikibaseCount
			}
		}
	}
}
```

Result:

```json
{
  "data": {
    "aggregateSoftwarePopularity": {
      "meta": {
        "totalCount": 12
      },
      "data": [
        {
          "softwareName": "MediaWiki",
          "wikibaseCount": 41,
          "versions": [
            {
              "version": "1.41.0",
              "versionDate": "2024-02-07T06:39:00",
              "versionHash": "5498056",
              "wikibaseCount": 3
            },
            ...
          ]
        },
        ...
        {
          "softwareName": "ICU",
          "wikibaseCount": 40,
          "versions": [
            {
              "version": "67.1",
              "versionDate": null,
              "versionHash": null,
              "wikibaseCount": 11
            },
            {
              "version": "72.1",
              "versionDate": null,
              "versionHash": null,
              "wikibaseCount": 6
            },
            ...
          ]
        },
        ...
      ]
    }
  }
}
```

### Aggregated Language Popularity:

Aggregated from the manually-entered languages above. The data is paginated as above in Wikibase List; the Page Number and Page Size arguments are the same, and the queries return Meta and Data as above.

- Language
- Primary Wikibases: Number of Wikibases with this as their primary languages
- Additional Wikibases: Number of Wikibases with this as an additional language
- Total Wikibases: Number of Wikibase with this as a primary or additional language

The data is ordered by Primary Wikibases descending, then Total Wikibases descending, then alphabetically by Language

#### Example:

Query:

```graphql
query MyQuery($pageNumber: Int!, $pageSize: Int!) {
	aggregateLanguagePopularity(pageNumber: $pageNumber, pageSize: $pageSize) {
		meta {
			pageNumber
			pageSize
			totalCount
			totalPages
		}
		data {
			language
			primaryWikibases
			additionalWikibases
			totalWikibases
		}
	}
}
```

Result:

```json
{
  "data": {
    "aggregateLanguagePopularity": {
      "meta": {
        "pageNumber": 1,
        "pageSize": 20,
        "totalCount": 16,
        "totalPages": 1
      },
      "data": [
        {
          "language": "English",
          "primaryWikibases": 28,
          "additionalWikibases": 3,
          "totalWikibases": 31
        },
        {
          "language": "German",
          "primaryWikibases": 5,
          "additionalWikibases": 3,
          "totalWikibases": 8
        },
        ...
        {
          "language": "Svenska",
          "primaryWikibases": 0,
          "additionalWikibases": 1,
          "totalWikibases": 1
        }
      ]
    }
  }
}
```

### Aggregated Property Popularity:

Aggregated from the Property Popularity Observations above. The data is paginated as above in Wikibase List; the Page Number and Page Size arguments are the same, and the queries return Meta and Data as above.

- Property URL
- Usage Count: Sum of usages in all Wikibases
- Wikibase Count: Number of Wikibases that use this property

The data is ordered by Wikibase Count descending, then Usage Count descending, then alphabetically by Property URL

#### Example:

Query:

```graphql
query MyQuery {
	aggregatePropertyPopularity(pageNumber: 1, pageSize: 10) {
		meta {
			totalCount
		}
		data {
			propertyUrl
			usageCount
			wikibaseCount
		}
	}
}
```

Result:

```json
{
  "data": {
    "aggregatePropertyPopularity": {
      "meta": {
        "totalCount": 79501
      },
      "data": [
        {
          "propertyUrl": "http://schema.org/description",
          "usageCount": 3149752997,
          "wikibaseCount": 17
        },
        {
          "propertyUrl": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
          "usageCount": 1944635733,
          "wikibaseCount": 17
        },
        ...
      ]
    }
  }
}
```

### Aggregated Quantity:

Data aggregated from the Quantity Observations above.

#### Example:

Query:

```graphql
query MyQuery {
	aggregateQuantity {
		totalItems
		totalLexemes
		totalProperties
		totalTriples
		wikibaseCount
	}
}
```

Result:

```json
{
	"data": {
		"aggregateQuantity": {
			"totalItems": 123291236,
			"totalLexemes": 1314076,
			"totalProperties": 20368,
			"totalTriples": 17745095804,
			"wikibaseCount": 17
		}
	}
}
```

### Aggregated Statistics:

Aggregated from the Statistics Observations above. As indicated above, averages (edits per page and words per content page) are calculated at query time.

#### Example:

Query:

```graphql
query MyQuery {
	aggregateStatistics {
		wikibaseCount
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
```

Result:

```json
{
	"data": {
		"aggregateStatistics": {
			"wikibaseCount": 39,
			"edits": {
				"editsPerPageAvg": 4.912389909272705,
				"totalEdits": 102551430
			},
			"files": {
				"totalFiles": 107936
			},
			"pages": {
				"contentPageWordCountAvg": 5.910143746962713,
				"contentPageWordCountTotal": 23289542,
				"contentPages": 3940605,
				"totalPages": 20876077
			},
			"users": {
				"activeUsers": 912,
				"totalAdmin": 347,
				"totalUsers": 284827
			}
		}
	}
}
```

### Aggregated Users:

Data aggregated ffrom the User Observations above.

#### Example:

Query:

```graphql
query MyQuery {
	aggregateUsers {
		totalAdmin
		totalUsers
		wikibaseCount
	}
}
```

Result:

```json
{
	"data": {
		"aggregateUsers": {
			"totalAdmin": 366,
			"totalUsers": 227834,
			"wikibaseCount": 43
		}
	}
}
```
