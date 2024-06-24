"""SPARQL Queries"""

from fetch_data.sparql_data.sparql_queries.count_items import COUNT_ITEMS_QUERY
from fetch_data.sparql_data.sparql_queries.count_lexemes import COUNT_LEXEMES_QUERY
from fetch_data.sparql_data.sparql_queries.count_properties import (
    COUNT_PROPERTIES_QUERY,
)
from fetch_data.sparql_data.sparql_queries.item_links import (
    ITEM_LINKS_QUERY,
    ItemLink,
    clean_item_link_data,
)
from fetch_data.sparql_data.sparql_queries.item_property_counts import (
    ITEM_PROPERTY_COUNTS_QUERY,
)
from fetch_data.sparql_data.sparql_queries.property_usage import PROPERTY_USAGE_QUERY
