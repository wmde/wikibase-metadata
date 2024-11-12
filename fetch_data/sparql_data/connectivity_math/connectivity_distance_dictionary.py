"""Compile Connectivity Distance"""

from collections.abc import Iterable
from tqdm import tqdm


def compile_distance_dict(
    all_nodes: Iterable[str], link_dict: dict[str, set[str]]
) -> dict[str, dict[str, int]]:
    """Compile Distance Dictionary

    Dictionary of all direct and indirect connections in the data,
    with each node having a dictionary of all nodes it connects to,
    and the number of links it takes to make that connection.

    `[a, b, c], {a: {b}, b: {a, c}}`

    becomes

    `{a: {b: 1, c: 2}, b: {a: 1, c: 1}, c: {}}`
    """

    distance_dict: dict[str, dict[str, int]] = {}

    for node in tqdm(all_nodes):
        distance_dict[node] = {node: 0}
        returning = True
        step = 1
        while returning:
            step_list = next_step(link_dict, distance_dict[node].keys()) - set(
                distance_dict[node].keys()
            )
            returning = len(step_list) > 0
            for n in step_list:
                distance_dict[node][n] = step
            step += 1
    return distance_dict


def next_step(link_dict: dict[str, set[str]], node_list: Iterable[str]) -> set[str]:
    """Return all nodes any node in the list is linked to"""

    return {n for node in node_list for n in link_dict[node]}
