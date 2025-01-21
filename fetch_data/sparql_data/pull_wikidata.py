"""Get SPARQL Data from Wikidata"""

import asyncio
from datetime import datetime
from json import JSONDecodeError
import os
import sys
from SPARQLWrapper import QueryResult, SPARQLWrapper, JSON

from logger import logger


async def get_sparql_results(endpoint_url: str, query: str, query_name: str) -> dict:
    """Get SPARQL Data from Wikidata ASYNC"""
    return await asyncio.to_thread(
        _get_results, endpoint_url=endpoint_url, query=query, query_name=query_name
    )


# retrieve results from a given endpoint given a distinct SPARQL query
def _get_results(endpoint_url: str, query: str, query_name: str) -> dict:
    """Get SPARQL Data from Wikidata"""
    user_agent = f"WDQS-example Python/{sys.version_info[0]}.{sys.version_info[1]}"
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent, returnFormat=JSON)
    sparql.setQuery(query)
    query_result: QueryResult = sparql.query()
    try:
        return query_result.convert()
    except JSONDecodeError as exc:
        logger.warning(
            "SPARQLError",
            stack_info=True,
            extra={
                "query": query,
                "endpoint": endpoint_url,
                "result": str(query_result),
                "exception": str(exc),
            },
        )
        failed_dir = (
            f"fetch_data/sparql_data/sparql_queries/failed_queries/{query_name}"
        )
        os.makedirs(failed_dir, exist_ok=True)
        with open(
            f"{failed_dir}/temp_{datetime.now()}.txt", "w", encoding="utf-8"
        ) as temp:
            temp.write(str(query_result))
        raise exc
