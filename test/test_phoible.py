# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test PHOIBLE assertions."""

from csv import reader
from pathlib import Path


def test_each_phoneme_has_unique_feature_vector(phoible: Path) -> None:
    """Each phoneme should have only one feature vector."""
    phonemes: dict[str, set[tuple[str, ...]]] = {}
    with open(phoible, encoding="utf-8") as file:
        rows = reader(file)
        next(rows)
        for row in rows:
            phoneme = row[6]
            features = row[11:]
            phonemes.setdefault(phoneme, set()).add(tuple(features))

    for vectors in phonemes.values():
        assert len(vectors) == 1


def diff(first: tuple[str, ...], second: tuple[str, ...]) -> list[int]:
    """Return list of indices where first and second tuples differ."""
    assert len(first) == len(second)
    return [i for i, (a, b) in enumerate(zip(first, second)) if a != b]


def test_segments_with_pipe(phoible: Path) -> None:
    """If A|B is a segment, then the feature vectors of A, B and A|B should not
    be too different.
    """
    phonemes = {}
    with open(phoible, encoding="utf-8") as file:
        rows = reader(file)
        next(rows)
        for row in rows:
            phoneme = row[6]
            phonemes[phoneme] = tuple(row[11:])

    for phoneme, features in phonemes.items():
        if "|" not in phoneme:
            continue

        vectors = [features]

        left, right = phoneme.split("|")
        if left in phonemes:
            vectors.append(phonemes[left])
        if right in phonemes:
            vectors.append(phonemes[right])

        # Compare every pair of vector.
        for i in range(1, len(vectors)):
            for j in range(i):
                difference = diff(vectors[i], vectors[j])

                # The difference is actually almost always 1, except for
                # /t̪s̪ɦ|tsɦ/.
                assert len(difference) <= 2

                # Segments with pipe combine phonemes that differ in features
                # 17 to 19 (coronal, anterior or distributed).
                for feature in difference:
                    assert 17 <= feature <= 19


def test_there_are_invalid_segments(
    phoible: Path,
    invalid_segments: list[str],
) -> None:
    """PHOIBLE has some invalid segments.

    Future updates to PHOIBLE may make this test obsolete.
    """
    assert invalid_segments

    not_found = set(invalid_segments)
    lines = phoible.read_text(encoding="utf-8").splitlines()

    for line in lines:
        found = {segment for segment in invalid_segments if segment in line}
        not_found.difference_update(found)

    assert not not_found
