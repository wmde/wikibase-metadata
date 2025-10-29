"""Compile User Data"""

from fetch_data.utils import counts


def compile_all_implicit_user_groups(data: list[dict]) -> set[str]:
    """Compile set of implicit groups"""
    return {group for user in data for group in user["implicitgroups"]}


def compile_user_group_counts(data: list[dict]) -> dict:
    """Return dict: {group_name: user_count}"""
    return counts([group for user in data for group in set(user["groups"])])
