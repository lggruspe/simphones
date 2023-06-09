# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test PHOIBLE assertions."""

from pathlib import Path
import re
import typing as t


Row: t.TypeAlias = tuple[str, ...]


def test_each_phoneme_has_unique_feature_vector(
    phoible_rows: list[Row],
) -> None:
    """Each phoneme should have only one feature vector."""
    phonemes: dict[str, set[tuple[str, ...]]] = {}
    for row in phoible_rows:
        phoneme = row[6]
        features = row[11:]
        phonemes.setdefault(phoneme, set()).add(tuple(features))

    for vectors in phonemes.values():
        assert len(vectors) == 1


def diff(first: tuple[str, ...], second: tuple[str, ...]) -> list[int]:
    """Return list of indices where first and second tuples differ."""
    assert len(first) == len(second)
    return [i for i, (a, b) in enumerate(zip(first, second)) if a != b]


def test_segments_with_pipe(phoible_rows: list[Row]) -> None:
    """If A|B is a segment, then the feature vectors of A, B and A|B should not
    be too different.
    """
    phonemes = {}
    for row in phoible_rows:
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


def test_language_codes(phoible_rows: list[Row]) -> None:
    """Make some assertions about language codes in PHOIBLE.

    Summary:
    - PHOIBLE doesn't use special ISO639-3 language codes.
    - PHOIBLE uses soem language codes reserved for local use (qaa-qtz).
    """
    found = set()
    for row in phoible_rows:
        glottocode = row[1]
        iso639_3 = row[2]

        assert glottocode != ""

        # mis, mul, und and zxx are special language codes.
        # See https://en.wikipedia.org/wiki/ISO_639-3#Special_codes.
        assert iso639_3 not in ("", "mis", "mul", "und", "zxx")

        if re.match("^q[a-t]", iso639_3):
            found.add(iso639_3)

    # Found some language codes reserved for local use.
    assert found


def test_language_code_counts(phoible_rows: list[Row]) -> None:
    """Make some assertions about language code counts in PHOIBLE."""
    missing_glottocode = set()
    missing_iso639_3 = set()
    missing_name = set()

    for row in phoible_rows:
        glottocode = row[1]
        iso639_3 = row[2]
        name = row[3]

        language = (glottocode, iso639_3, name)

        if glottocode in ("", "NA"):
            missing_glottocode.add(language)
        if iso639_3 in ("", "NA"):
            missing_iso639_3.add(language)
        if name in ("", "NA"):
            missing_name.add(language)

    assert not missing_name
    assert len(missing_glottocode) <= 2
    assert len(missing_iso639_3) <= 38


def test_glottocodes_iso639_3_mapping(phoible_rows: list[Row]) -> None:
    """Each glottocode should map to only one ISO639-3 code."""
    glottocodes: dict[str, set[str]] = {}

    for row in phoible_rows:
        glottocode = row[1]
        iso639_3 = row[2]

        # Skip languages that don't have a Glottocode or a ISO639-3 code.
        if glottocode in ("", "NA"):
            continue
        if iso639_3 in ("", "NA"):
            continue

        glottocodes.setdefault(glottocode, set()).add(iso639_3)

    for values in glottocodes.values():
        assert len(values) == 1
