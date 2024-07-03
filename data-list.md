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


  
