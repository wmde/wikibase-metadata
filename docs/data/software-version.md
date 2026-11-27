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
