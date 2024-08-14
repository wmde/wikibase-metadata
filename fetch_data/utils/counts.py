"""Counts"""

from typing import Iterable, TypeVar


T = TypeVar("T")


def counts(values: Iterable[T]) -> dict[T, int]:
    """Count instances of each value
    @return dict {value: count_values}"""

    result: dict[T, int] = {}
    for value in sorted(values):
        if value not in result:
            result[value] = 0
        result[value] += 1
    return result
