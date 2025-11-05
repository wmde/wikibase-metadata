"""Constants"""

DATA_DIRECTORY = "tests/test_upsert_cloud_instances/data"

WIKIBASE_LIST_QUERY = """
query MyQuery {
  wikibaseList(pageNumber: 1, pageSize: 10000) {
    data {
      id
      wikibaseType
      urls {
        baseUrl
      }
    }
  }
}
"""
