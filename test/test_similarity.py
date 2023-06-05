# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test simphones.similarity."""

from simphones.similarity import compute_similarity


def test_compute_similarity_relationship_with_distances() -> None:
    """Similarity and distance should have a negative relationship."""
    distances = {
        ("m", "n"): 0.2,
        ("n", "ŋ"): 0.8,
    }
    similarity = compute_similarity(distances)

    pair1 = ("m", "n")
    pair2 = ("n", "ŋ")
    assert distances[pair1] < distances[pair2]
    assert similarity[pair1] > similarity[pair2]
