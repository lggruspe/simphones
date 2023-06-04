# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Serialization tools."""

from csv import reader, writer
from json import dumps
from pathlib import Path

from simphones.distances import unordered
from simphones.normalize import normalize_ipa
from simphones.similarity import SimilarityData


class MalformedDataset(Exception):
    """Raised when reading a file that doesn't contain similarity data."""


def save_as_csv(
    path: Path,
    similarity: SimilarityData,
    ndigits: int | None = None,
) -> None:
    """Save similarity data as a CSV file.

    `ndigits` is the precision to round similarity scores to.
    Set to `None` to disable rounding.
    """
    with open(path, "w", encoding="utf-8") as file:
        csv_file = writer(file)
        for (phone1, phone2), score in similarity.items():
            if phone1 == phone2:
                continue
            assert phone1 < phone2

            rounded = score
            if ndigits is not None:
                rounded = round(score, ndigits=ndigits)

            row = (phone1, phone2, rounded)
            csv_file.writerow(row)


def save_as_json(
    path: Path,
    similarity: SimilarityData,
    ndigits: int | None = None,
) -> None:
    """Save similarity data as a JSON file.

    `ndigits` is the precision to round similarity to.
    Set to `None` to disable rounding.
    """
    data = {}
    for (phone1, phone2), score in similarity.items():
        if phone1 == phone2:
            continue
        assert phone1 < phone2

        rounded = score
        if ndigits is not None:
            rounded = round(score, ndigits=ndigits)

        data[f"{phone1} {phone2}"] = rounded

    text = dumps({"similarity": data}, ensure_ascii=False)
    path.write_text(text, encoding="utf-8")


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


__all__ = ["read_from_csv", "save_as_csv", "save_as_json"]
