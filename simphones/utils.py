# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Serialization tools."""

from csv import reader, writer
from pathlib import Path

from simphones.normalize import normalize_ipa
from simphones.similarity import SimilarityData, unordered


class MalformedDataset(Exception):
    """Raised when reading a file that doesn't contain similarity data."""


def save_as_csv(path: Path, similarity: SimilarityData) -> None:
    """Save similarity data as a CSV file."""
    with open(path, "w", encoding="utf-8") as file:
        csv_file = writer(file)
        for (phone1, phone2), score in similarity.items():
            csv_file.writerow((phone1, phone2, score))


def read_from_csv(path: Path) -> SimilarityData:
    """Read similarity data from CSV file.

    May raise `MalformedDataset`.
    """
    similarity = {}
    with open(path, encoding="utf-8") as file:
        rows = reader(file)
        for row in rows:
            if len(row) != 3:
                raise MalformedDataset

            phone1, phone2, token = row
            try:
                score = float(token)
            except ValueError as exc:
                raise MalformedDataset from exc

            pair = unordered(normalize_ipa(phone1), normalize_ipa(phone2))
            similarity[pair] = score
    return similarity


__all__ = ["read_from_csv", "save_as_csv"]
