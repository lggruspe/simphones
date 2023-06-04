# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
# pylint: disable=invalid-name
"""Compute distances between sounds."""


from collections import Counter
import typing as t

import networkx as nx   # type: ignore

from simphones.inventories import InventoryDataset, Phone


Cooccurrence: t.TypeAlias = tuple[Phone, Phone]
DistanceData: t.TypeAlias = dict[Cooccurrence, float]


def compute_distances(inventories: InventoryDataset) -> DistanceData:
    """Compute distance for every pair of sounds."""
    graph = create_allophone_graph(inventories)

    assert not [node for node, degree in graph.degree() if degree == 0]

    # Temporarily remove nodes of degree 1 to reduce the size of the graph for
    # the next step.
    backup = set()
    for node, degree in graph.degree():
        if degree == 1:
            neighbor = next(graph.neighbors(node))
            assert node != neighbor

            weight = graph.edges[(node, neighbor)]["weight"]
            backup.add((node, neighbor, weight))
    graph.remove_nodes_from(node for node, _, _ in backup)

    # Compute shortest path lengths between sounds.
    distances = shortest_path_lengths(graph)

    # Compute distances for removed edges.
    for node, neighbor, weight in backup:
        distances[unordered(node, neighbor)] = weight

    # Iterate through paths node ~> neighbor ~> target.
    # The path from node ~> neighbor is already known, because they're just
    # adjacent nodes.
    for node, neighbor, weight in backup:
        for target in graph.nodes:
            if target in (node, neighbor):
                continue

            path = unordered(neighbor, target)
            if path not in distances:
                continue
            distance = distances[path]

            path = unordered(node, target)
            distances[path] = weight + distance
    return distances


def create_allophone_graph(inventories: InventoryDataset) -> nx.Graph:
    """Create a weighted graph of allophones.

    Nodes represent phones. Two nodes are connected if they are allophones in
    some language. The edge weight equals the "distance" between the two
    phones.
    """
    cooccurrences = count_cooccurrences(inventories)
    allophones = count_allophones(inventories)
    graph = nx.Graph()

    for (a, b), count in allophones.most_common():
        if a == b:
            continue

        count_a = allophones[(a, a)]
        count_b = allophones[(b, b)]

        assert count_a == cooccurrences[(a, a)]
        assert count_b == cooccurrences[(b, b)]

        weight = 1 - count/(count_a + count_b - cooccurrences[(a, b)])
        assert 0 <= weight <= 1
        graph.add_edge(a, b, weight=weight)
    return graph


def unordered(a: Phone, b: Phone) -> Cooccurrence:
    """Sort the phones."""
    if b < a:
        a, b = b, a
    return (a, b)


def count_cooccurrences(
    inventories: InventoryDataset,
) -> Counter[Cooccurrence]:
    """Count how many times each pair of phones occur in the same language.

    A phone is considered to cooccur with itself, so `counter[(phone, phone)]`
    is the number of languages in which the phone occurs.
    Since cooccurrence is symmetric, only pairs `(phone1, phone2)` with
    `phone1 <= phone2` are counted.
    """
    counter: Counter[Cooccurrence] = Counter()
    for inventory in inventories.values():
        phones = list(inventory.keys())
        n = len(phones)

        for i in range(n):
            for j in range(i+1):
                cooccurrence = unordered(phones[i], phones[j])
                counter[cooccurrence] += 1
    return counter


def count_allophones(inventories: InventoryDataset) -> Counter[Cooccurrence]:
    """Count languages that have a pair of phones as allophones.

    Only pairs `(phone1, phone2)` with `phone1 <= phone2` are counted.
    """
    counter: Counter[Cooccurrence] = Counter()
    for inventory in inventories.values():
        for phone, allophones in inventory.items():
            assert phone in allophones  # Check symmetry.

            for allophone in allophones:
                assert allophone in inventory   # Check symmetry.
                if phone <= allophone:
                    counter[(phone, allophone)] += 1
    return counter


def shortest_path_lengths(graph: nx.Graph) -> dict[Cooccurrence, float]:
    """Compute length of shortest path between every pair of nodes.

    The return value is a dictionary keyed by tuples of graph nodes.
    Since the graph is undirected, only one entry is included for each pair of
    nodes.
    Assume `phone1 <= phone2` if `(phone1, phone2)` is in the dictionary.
    """
    result = {}
    distances = nx.all_pairs_dijkstra_path_length(graph)

    for source, targets in distances:
        for target, distance in targets.items():
            if source <= target:
                result[(source, target)] = distance
    return result


__all__ = ["compute_distances"]
