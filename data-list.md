## aggregated

- list of all known instances
- meta (pagination mechanism for navigating database)
  - pageNumber (var for paginating)
  - pageSize (var for paginating)
  - totalCount (total number of known instances)
  - totalPages (total instances divided across page numbers by size)
- aggregateSoftwarePopularity (note: being reworked) includes skin, libraries, extensions
  - softwareName
  - version
  - versionData
- property popularity

## individual instances

### manually generated

- titles
- org
- location
  - country
  - region
- urls
  - actionApi
  - baseUrl
  - indexApi
  - sparqlEndpointUrl (machine endpoint)
  - sparqlUrl (human UI)
  - SpecialVersionUrl

### automatically generated

#### general notes:

all entries can be filtered by

- most recent
- all observations

date meta data is captured on each data collection

#### categories:

data modelling :

- connectivity (see connectivity_notes.txt)
  - averageConnectedDistance
  - connectivity
  - relationship item counts
  - objects
  - total number of links
  - total unique connections (total non zero connections; countif > 0)
- property popularity (all triples, in how many is X the linking property)

data volume:

- quantity (note: has potential to track changes over time)
  - totalItems
  - totalLexemes
  - totalProperties

software versions:

- extensions, libraries, skins, software
  - softwareName
  - version (inconsistent: can be semvar, partial, docker tag, hash, null)
  - versionDate
  - versionHash

User observations:

- total users
- list of all groups
  - group
    - groupName
    - wikibaseDefault
    - implicit (new users automatically added)
    - userCount

## Individual Wikibase Instances:

### Manually Added Attributes:

- Title
- Organization
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

```
query MyQuery {
  wikibase(wikibaseId: 10) {
    id
    title
    organization
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

```
{
  "data": {
    "wikibase": {
      "id": "10",
      "title": "ELTEdata",
      "organization": "Digital Humanities Department of ELTE BTK (Eötvös Loránd University Faculty of Humanities)",
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

For each type of observation, the most recent successful observation -- maximum `observationDate` where `returnedData = True` -- is returned as `mostRecent`, and all observations, successful or not, are returned in a collection labelled `allObservations`. `mostRecent` will be `null` if there are no successful observations.

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

```
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

```
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

### Property Popularity Observations:

Using SPARQL, we query for all properties in the Wikibase, and the number of times they are used in the data. We return that list.

- Property URL: the format the properties are returned in, as many are not specific to this particular wikibase
- Usage Count: Number of times the property is used

#### Example:

Query:

```
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

```
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

#### Example:

Query:

```
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

```
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

### Software Version Observations:

This data is parsed from the Wikibase's Special:Version page. For each installed software (Mediawiki, Elasticsearch, etc), skin, library, and extension, the following fields are fetched:

- Software Name
- Version: If any identifiable version string exists in the table row; may be semver, date, docker-tag-like string, hash, a combination, or nothing
- Version Date: If any identifiable, parsable date exists in the table row
- Version Hash: If any identifiable commit hash exists in the table row


#### Example:

Query:

```
query MyQuery {
  wikibase(wikibaseId: 43) {
    id
    softwareVersionObservations {
      mostRecent {
        id
        observationDate
        returnedData
        installedExtensions {
          ...WikibaseSoftwareVersionStrawberryModelFragment
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
  softwareName
  version
  versionDate
  versionHash
}
```

Result:

```
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
              "softwareName": "Babel",
              "version": "1.12.0",
              "versionDate": null,
              "versionHash": null
            },
            {
              "id": "13948",
              "softwareName": "CLDR",
              "version": "4.10.0",
              "versionDate": null,
              "versionHash": null
            },
            ...
          ],
          "installedLibraries": [
            {
              "id": "13955",
              "softwareName": "christian-riesen/base32",
              "version": "1.4.0",
              "versionDate": null,
              "versionHash": null
            },
            {
              "id": "13956",
              "softwareName": "composer/installers",
              "version": "1.12.0",
              "versionDate": null,
              "versionHash": null
            },
            ...
          ],
          "installedSkins": [
            {
              "id": "13930",
              "softwareName": "Vector",
              "version": null,
              "versionDate": null,
              "versionHash": null
            }
          ],
          "installedSoftware": [
            {
              "id": "13928",
              "softwareName": "Elasticsearch",
              "version": "6.8.23",
              "versionDate": null,
              "versionHash": null
            },
            {
              "id": "13927",
              "softwareName": "ICU",
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