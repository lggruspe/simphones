# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
# pylint: disable=invalid-name
"""Compute phone similarity from PHOIBLE allophone data."""

from collections import Counter
import typing as t

import networkx as nx   # type: ignore

from simphones.inventories import InventoryDataset, Phone


Cooccurrence: t.TypeAlias = tuple[Phone, Phone]
SimilarityData: t.TypeAlias = dict[Cooccurrence, float]


def compute_similarity(inventories: InventoryDataset) -> SimilarityData:
    """Compute similarity for every pair of sounds."""
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

    # Partially compute similarity using the allophone graph.
    similarity = maximize_products(graph)

    # Compute similarity for removed edges.
    for node, neighbor, weight in backup:
        similarity[unordered(node, neighbor)] = weight

    # Iterate through paths node ~> neighbor ~> target.
    # The path from node ~> neighbor is already known, because they're just
    # adjacent nodes.
    for node, neighbor, weight in backup:
        for target in graph.nodes:
            if target in (node, neighbor):
                continue

            path = unordered(neighbor, target)
            if path not in similarity:
                continue
            probability = similarity[path]

            path = unordered(node, target)
            similarity[path] = weight * probability
    return similarity


def maximize_products(graph: nx.Graph) -> SimilarityData:
    """Compute similarity between pairs of nodes.

    Similarity is expressed as a probability.
    Assumption: P(A ~ C) = max P(A ~ B) * P(B ~ C).
    Allophone probabilities are used as a proxy for similarity.

    Since similarity is symmetric, only one entry is created for each pair of
    phones.
    """
    # Initialize probabilities with allophone probabilities.
    probabilities = {}
    for (source, target), data in graph.edges.items():
        probabilities[unordered(source, target)] = data["weight"]

    # Based on Floyd-Warshall algorithm, but finds max probability products
    # instead of minimum distances.
    # Iterates through paths x ~> y ~> z.
    for x in graph.nodes:
        for y in graph.nodes:
            if x == y:
                continue

            key_xy = unordered(x, y)
            if key_xy not in probabilities:
                # There's no path from x to y.
                continue

            probability_xy = probabilities[key_xy]

            for z in graph.nodes:
                if z in (x, y):
                    continue

                key_yz = unordered(y, z)
                if key_yz not in probabilities:
                    # There's no path from y to z.
                    continue
                probability_yz = probabilities[key_yz]

                key_xz = unordered(x, z)
                if key_xz not in probabilities:
                    # Add a path x ~> y ~> z.
                    probabilities[key_xz] = probability_xy * probability_yz
                    continue

                # There's a path x ~> y ~> z.
                probabilities[key_xz] = max(
                    probabilities[key_xz],
                    probability_xy * probability_yz,
                )
    return probabilities


def create_allophone_graph(inventories: InventoryDataset) -> nx.Graph:
    """Create a weighted graph of allophones.

    Nodes represent phones. Two nodes are connected if they are allophones in
    some language. The edge weight equals the probability that the two phones
    are allophones.
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

        # The probability is computed over languages that contain `a` or `b`.
        # It should be equal to 1 when a == b.
        weight = count/(count_a + count_b - cooccurrences[(a, b)])

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


__all__ = ["compute_similarity"]
