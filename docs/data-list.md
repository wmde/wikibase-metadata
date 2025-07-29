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
        "additional": [
          "English",
          "German",
          "Japanese",
          "Spanish"
        ]
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

The relationship between `mostRecent` and `allObservations` is demonstrated below in Connectivity Observations, but omitted elsewhere for brevity.

### Connectivity Observations:

Please see connectivity_notes for further details.

We want to measure the connectivity of the network of Wikidata items in the Wikibase. Using SPARQL, we query the Wikibase for direct links between Wikidata items. We then calculate the following:

- Returned Links: total number of links returned in our query. NOT UNIQUE.
- Total Connections: total number of connections between items, direct or indirect\*
- Average Connection Distance: Say a returned link `a -> b` has length `1`. An indirect\* connection using two such returned links, `a -> b -> c` then has length `2`. This figure represents the average length of _all_ connections, direct or indirect.
- Connectivity - In theory, each item could link to every other item in the network. So we take the actual number of connections and divide by the number of possible connections: `k / (n * (n - 1))`, where `k` is the number of connections (direct or indirect) and `n` is the total number of items.
- Relationship Item Counts: If we retrieve `a -> b, a -> c`, we say that the item `a` links to `2` objects, and items `b` and `c` link to `0` objects. We then aggregate further and say that `1` item has `2` relationships and `2` items have `0` relationships.
- Relationship Object Counts: If we retrieve `a -> b, a -> c`, we say that the object `a` is linked to by `0` items, the object `b` is linked to by `1` item, and the object `c` is linked to by `1` item. We then aggregate further and say that `1` object has `0` relationships and `2` objects have `1` relationship.

\* The SPARQL query returns directional links `a -> b`, so we say there's a direct connection between `a` and `b`. If `b -> c` is also returned, then we say `a` is _indirectly_ connected to `c`: `a -> b -> c`. Note that when we say directional, we mean that we do not _assume_ `b -> a` if `a -> b`; we would need a separate `b -> a` connection.

#### Example:

Query:

```graphql
query MyQuery {
  wikibase(wikibaseId: 43) {
    id
    connectivityObservations {
      mostRecent {
        ...WikibaseConnectivityObservationStrawberryModelFragment
      }
      allObservations {
        ...WikibaseConnectivityObservationStrawberryModelFragment
      }
    }
  }
}

fragment WikibaseConnectivityObservationStrawberryModelFragment on WikibaseConnectivityObservationStrawberryModel {
  id
  observationDate
  returnedData
  returnedLinks
  totalConnections
  averageConnectedDistance
  connectivity
  relationshipItemCounts {
    relationshipCount
    itemCount
  }
  relationshipObjectCounts {
    relationshipCount
    objectCount
  }
}
```

Result:

```json
{
  "data": {
    "wikibase": {
      "id": "43",
      "connectivityObservations": {
        "mostRecent": {
          "id": "12",
          "observationDate": "2024-06-24T09:01:31",
          "returnedData": true,
          "returnedLinks": 210,
          "totalConnections": 205,
          "averageConnectedDistance": 1.725531914893617,
          "connectivity": 0.06429548563611491,
          "relationshipItemCounts": [
            {
              "relationshipCount": 0,
              "itemCount": 2
            },
            {
              "relationshipCount": 1,
              "itemCount": 38
            },
            ...
          ],
          "relationshipObjectCounts": [
            {
              "relationshipCount": 0,
              "objectCount": 36
            },
            {
              "relationshipCount": 1,
              "objectCount": 28
            },
            ...
          ]
        },
        "allObservations": [
          {
            "id": "1",
            "observationDate": "2024-06-20T12:13:08",
            "returnedData": true,
            "returnedLinks": 210,
            ...
          },
          {
            "id": "6",
            "observationDate": "2024-06-20T16:48:27",
            "returnedData": true,
            "returnedLinks": 210,
            ...
          },
          ...
        ]
      }
    }
  }
}
```

Data abbreviated for brevity.

### Log Observations:

Using the Action API, we query for the first log and the last 30 days'.

- First Log:
  - Date
- Last Log:
  - Date
  - User Type: Bot, Missing, None, User
- Last Month:
  - All Users: Count distinct users
  - Human Users: Count distinct (probably) human users
  - Log Count

#### Example:

Query:

```graphql
query MyQuery {
  wikibase(wikibaseId: 10) {
    logObservations {
      mostRecent {
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
        lastMonth {
          allUsers
          humanUsers
          logCount
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
      "logObservations": {
        "mostRecent": {
          "id": "39",
          "observationDate": "2024-07-03T21:18:08",
          "returnedData": true,
          "firstLog": {
            "date": "2021-03-19T09:20:21"
          },
          "lastLog": {
            "date": "2024-07-03T14:45:01",
            "userType": "BOT"
          },
          "lastMonth": {
            "allUsers": 2,
            "humanUsers": 1,
            "logCount": 387
          }
        }
      }
    }
  }
}
```

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

### Software Version Observations:

This data is parsed from the Wikibase's Special:Version page. For each installed software (MediaWiki, Elasticsearch, etc), skin, library, and extension, the following fields are fetched:

- Software Name
- Version: If any identifiable version string exists in the table row; may be semver, date, docker-tag-like string, hash, a combination, or nothing
- Version Date: If any identifiable, parsable date exists in the table row
- Version Hash: If any identifiable commit hash exists in the table row

For Extensions, if possible, the server will pull additional data from MediaWiki.org after completing the observation, including:

- MediaWiki Extension URL
- Description
- Tags
- Latest Version
- Archived: If the extension has been noted as archived
- MediaWiki Bundled: If the extension is bundled with MediaWiki
- Public Wiki Count: MW keeps a record from WikiApiary of public wikis that include the extension
- Quarterly Download Count: Also pulled by MW from WikiApiary

#### Example:

Query:

```graphql
query MyQuery {
  wikibase(wikibaseId: 43) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedExtensions {
          id
          software {
            id
            softwareName
            softwareType
            fetched
            archived
            description
            latestVersion
            mediawikiBundled
            publicWikiCount
            quarterlyDownloadCount
            tags
            url
          }
          version
          versionDate
          versionHash
        }
        installedLibraries {
          ...WikibaseSoftwareVersionStrawberryModelFragment
        }
        installedSkins {
          ...WikibaseSoftwareVersionStrawberryModelFragment
        }
        installedSoftware {
          ...WikibaseSoftwareVersionStrawberryModelFragment
        }
      }
    }
  }
}

fragment WikibaseSoftwareVersionStrawberryModelFragment on WikibaseSoftwareVersionStrawberryModel {
  id
  software {
    id
    softwareName
  }
  version
  versionDate
  versionHash
}
```

Result:

```json
{
  "data": {
    "wikibase": {
      "id": "43",
      "softwareVersionObservations": {
        "mostRecent": {
          "id": "93",
          "observationDate": "2024-06-26T18:41:28",
          "returnedData": true,
          "installedExtensions": [
            {
              "id": "13933",
              "software": {
                "id": "17",
                "softwareName": "Babel",
                "softwareType": "EXTENSION",
                "fetched": "2024-10-30T10:51:10.173114",
                "archived": false,
                "description": "Adds a parser function to inform other users about language proficiency and categorize users of the same levels and languages.",
                "latestVersion": "Continuous updates",
                "mediawikiBundled": false,
                "publicWikiCount": 2416,
                "quarterlyDownloadCount": 61,
                "tags": [
                  "Parser function"
                ],
                "url": "https://www.mediawiki.org/wiki/Extension:Babel"
              },
              "version": "1.12.0",
              "versionDate": null,
              "versionHash": null
            },
            {
              "id": "13948",
              "software": {
                "id": "26",
                "softwareName": "CLDR",
                "softwareType": "EXTENSION",
                "fetched": "2024-10-30T10:51:15.841563",
                "archived": false,
                "description": "Provides functions to localize the names of languages, countries, currencies, and time units based on their language code.",
                "latestVersion": "4.14.0 (Continous updates)",
                "mediawikiBundled": false,
                "publicWikiCount": 6625,
                "quarterlyDownloadCount": null,
                "tags": [],
                "url": "https://www.mediawiki.org/wiki/Extension:CLDR"
              },
              "version": "4.10.0",
              "versionDate": null,
              "versionHash": null
            },
            ...
          ],
          "installedLibraries": [
            {
              "id": "13955",
              "software": {
                "id": "403",
                "softwareName": "christian-riesen/base32"
              },
              "version": "1.4.0",
              "versionDate": null,
              "versionHash": null
            },
            {
              "id": "13956",
              "software": {
                "id": "406",
                "softwareName": "composer/installers"
              },
              "version": "1.12.0",
              "versionDate": null,
              "versionHash": null
            },
            ...
          ],
          "installedSkins": [
            {
              "id": "13930",
              "software": {
                "id": "790",
                "softwareName": "Vector"
              },
              "version": null,
              "versionDate": null,
              "versionHash": null
            }
          ],
          "installedSoftware": [
            {
              "id": "13928",
              "software": {
                "id": "796",
                "softwareName": "Elasticsearch"
              },
              "version": "6.8.23",
              "versionDate": null,
              "versionHash": null
            },
            {
              "id": "13927",
              "software": {
                "id": "797",
                "softwareName": "ICU"
              },
              "version": "67.1",
              "versionDate": null,
              "versionHash": null
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

### Recent Changes:

Get the list of recent changes from a Wikibase instance. The [Recent Changes MediaWiki API is documented here](https://www.mediawiki.org/wiki/API:RecentChanges). A Recent Changes Observation is always calculated for the past 30 days. All change types are included; which are: `edit`, `new`, `log` and `categorize`. An Observation contains the following fields:

| Field                     | Description                                                                                                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `human_change_count`      | Number of changes made by humans as reported by the MediaWiki Recent Changes API when called with the `!bot` flag.                                                           |
| `human_change_user_count` | Number of unique users found in changes requested with `!bot` flag, derived from all usernames, IP addresses for anonymous edits as well as userid in the "userhidden case". |
| `bot_change_count`        | Number of changes made by bots as reported by the MediaWiki Recent Changes API when called with the `bot` flag.                                                              |
| `bot_change_user_count`   | Number of unique bots found in changes requested with `bot` flag, derived from all bot/usernames.                                                                            |
| `first_change_date`       | Date of first change, no matter if it was made by a human or bot.                                                                                                            |
| `last_change_date`        | Date of last change, no matter if it was made by a human or bot.                                                                                                             |

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
        botChangeCount
        botChangeUserCount
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
          "botChangeCount": 4,
          "botChangeUserCount": 1,
          "firstChangeDate": "2025-07-03T08:31:51",
          "lastChangeDate": "2025-07-25T15:41:47",
          "returnedData": true
        }
      }
    }
  }
}
```

