"""Links between items"""

import re
from typing import List


ITEM_LINKS_QUERY = """SELECT ?item ?object WHERE {
  ?item ?property ?object;
    wikibase:sitelinks [].
  ?object wikibase:sitelinks [].
}"""


class ItemLink:
    """Link from item to item"""

    item_from: str
    item_to: str

    def __init__(self, item_from: str, item_to: str):
        self.item_from = item_from
        self.item_to = item_to


def clean_value(val: str) -> str:
    """Remove Q-id from URL"""
    return re.sub(r".*/(Q\d+)", r"\1", val)


def clean_point(point: dict) -> ItemLink:
    """Coerce record into ItemLink"""

    return ItemLink(
        item_from=clean_value(point["item"]["value"]),
        item_to=clean_value(point["object"]["value"]),
    )


def clean_item_link_data(results: dict) -> List[ItemLink]:
    """Query Results to list of data"""

    return [clean_point(p) for p in results["results"]["bindings"]]
