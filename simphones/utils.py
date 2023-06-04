# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Serialization tools."""

from csv import reader, writer
from pathlib import Path

from simphones.distances import DistanceData, unordered
from simphones.normalize import normalize_ipa


class MalformedDataset(Exception):
    """Raised when reading a file that doesn't contain distance data."""


def save_as_csv(path: Path, distances: DistanceData) -> None:
    """Save distance data as a CSV file."""
    with open(path, "w", encoding="utf-8") as file:
        csv_file = writer(file)
        for (phone1, phone2), distance in distances.items():
            csv_file.writerow((phone1, phone2, distance))


def read_from_csv(path: Path) -> DistanceData:
    """Read distance data from CSV file.

    May raise `MalformedDataset`.
    """
    distances = {}
    with open(path, encoding="utf-8") as file:
        rows = reader(file)
        for row in rows:
            if len(row) != 3:
                raise MalformedDataset

            phone1, phone2, token = row
            try:
                distance = float(token)
            except ValueError as exc:
                raise MalformedDataset from exc

            pair = unordered(normalize_ipa(phone1), normalize_ipa(phone2))
            distances[pair] = distance
    return distances


__all__ = ["read_from_csv", "save_as_csv"]
