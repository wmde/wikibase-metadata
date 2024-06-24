"""Glacier Page"""

from math import ceil
from typing import Generic, List, TypeVar
import strawberry


T = TypeVar("T")


@strawberry.type
class PageMetadata:
    """Page Metadata"""

    page_number: int = strawberry.field(description="Page Number (1-indexed) - input")
    page_size: int = strawberry.field(description="Page Size - input")
    total_count: int = strawberry.field(description="Total Number of Records")
    total_pages: int = strawberry.field(description="Total Number of Pages")

    @classmethod
    def marshal(
        cls, page_number: int, page_size: int, total_count: int
    ) -> "PageMetadata":
        """Marshal Data into Page Metadata"""
        return cls(
            page_number=page_number,
            page_size=page_size,
            total_count=total_count,
            total_pages=ceil(total_count / page_size),
        )


@strawberry.type
class Page(Generic[T]):
    """Page"""

    meta: PageMetadata = strawberry.field(description="Metadata")
    data: List[T] = strawberry.field(description="Data")

    @classmethod
    def marshal(
        cls,
        page_number: int,
        page_size: int,
        total_count: int,
        page_data: List[T],
    ) -> "Page":
        """Marshal Data into Page"""
        return cls(
            meta=PageMetadata.marshal(
                page_number=page_number, page_size=page_size, total_count=total_count
            ),
            data=page_data,
        )
