# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Convert distances into a similarity score."""

import typing as t

from simphones.distances import Cooccurrence, DistanceData


SimilarityData: t.TypeAlias = dict[Cooccurrence, float]


def compute_similarity(distances: DistanceData) -> SimilarityData:
    """Convert distances into a similarity score."""
    max_distance = max(distances.values())

    assert max_distance > 0
    return {
        pair: distance/max_distance for pair, distance in distances.items()
    }


__all__ = ["compute_similarity"]
