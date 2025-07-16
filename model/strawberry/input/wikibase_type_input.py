"""Wikibase Type - INPUT"""

from typing import Optional
from model.enum.wikibase_type_enum import WikibaseType
import strawberry

from model.enum.wikibase_category_enum import WikibaseCategory
from model.strawberry.input.wikibase_url_input import WikibaseURLSetInput


@strawberry.input
class WikibaseTypeInput:
    """Include or Exclude Wikibase Types"""
    
    include: Optional[list[WikibaseType]]
    exclude: Optional[list[WikibaseType]]
