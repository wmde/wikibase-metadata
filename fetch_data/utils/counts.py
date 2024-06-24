"""Counts"""


def counts(values: list) -> dict:
    """Count instances of each value
    @return dict {value: count_values}"""

    result = {}
    for value in sorted(values):
        if value not in result:
            result[value] = 0
        result[value] += 1
    return result
