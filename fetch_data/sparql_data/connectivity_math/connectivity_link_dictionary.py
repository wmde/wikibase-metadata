"""Compile Link Dictionary"""

from collections.abc import Iterable
from fetch_data.sparql_data.sparql_queries import ItemLink


def compile_link_dict(
    clean_data: Iterable[ItemLink], all_nodes: Iterable[str], reverse: bool = False
) -> dict[str, set[str]]:
    """Compile Link Dictionary

    Direct links present in the data, represented as a dictionary,
    with each node having a set of all non-self nodes to which it directly links.

    `a -> b, a -> c, a -> d, b -> c, b -> a, d -> d`

    becomes

    `{a: {b, c, d}, b: {a, c}, c: {}, d: {}}`"""

    link_dict: dict[str, set[str]] = {}

    for node in all_nodes:
        link_dict[node] = set()
    for point in clean_data:
        link_dict[point.item_from if not reverse else point.item_to].add(
            point.item_to if not reverse else point.item_from
        )
    for node in all_nodes:
        link_dict[node].discard(node)
    return link_dict
