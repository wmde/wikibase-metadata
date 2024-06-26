"""Get Data from Wikidata"""

from datetime import datetime
from json import JSONDecodeError
import os
import sys
from SPARQLWrapper import SPARQLWrapper, JSON


# retrieve results from a given endpoint given a distinct SPARQL query
def get_results(endpoint_url: str, query: str, query_name: str) -> dict:
    """Get Data from Wikidata"""
    user_agent = f"WDQS-example Python/{sys.version_info[0]}.{sys.version_info[1]}"
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    query_result = sparql.query()
    try:
        return query_result.convert()
    except JSONDecodeError as exc:
        failed_dir = (
            f"fetch_data/sparql_data/sparql_queries/failed_queries/{query_name}"
        )
        os.makedirs(failed_dir, exist_ok=True)
        with open(
            f"{failed_dir}/temp_{datetime.now()}.txt", "w", encoding="utf-8"
        ) as temp:
            temp.write(str(query_result))
        raise exc
