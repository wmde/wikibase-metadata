"""Constants"""

DATA_DIRECTORY = "tests/test_update_missing_urls/data"


WIKIBASE_URLS_QUERY = """query MyQuery($wikibaseId: Int!) {
  wikibase(wikibaseId: $wikibaseId) {
    id
    urls {
      articlePath
      baseUrl
      scriptPath
      sparqlEndpointUrl
      sparqlFrontendUrl
      specialStatisticsUrl
    }
  }
}"""
