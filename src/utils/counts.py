def counts(values: list) -> dict:
    result = dict()
    for value in values:
        if value not in result.keys():
            result[value] = 0
        result[value] += 1
    return result
