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
