from src.utils.counts import counts


def compileAllUserGroups(data: list[dict]) -> set[str]:
    return {group for user in data for group in user["groups"]}


def compileAllImplicitUserGroups(data: list[dict]) -> set[str]:
    return {group for user in data for group in user["implicitgroups"]}


def compileUserGroupCounts(data: list[dict]) -> dict:
    return counts([group for user in data for group in user["groups"]])
