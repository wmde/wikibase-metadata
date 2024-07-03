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
