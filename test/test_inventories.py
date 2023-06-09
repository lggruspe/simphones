# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test simphones.inventories."""
from argparse import Namespace
import re

import pytest

from simphones.inventories import (
    get_phonological_inventories,
    get_sounds,
    main,
    parse_allophones,
)


def test_get_phonological_inventories() -> None:
    """The combined inventory should contain every other inventories."""
    inventories = get_phonological_inventories()

    phones1 = set(inventories["*"].keys())
    phones2: set[str] = set()

    for language, inventory in inventories.items():
        if language != "*":
            phones2.update(inventory.keys())

    assert phones2.issubset(phones1)
    # The reverse isn't necessarily true, because some languages in the PHOIBLE
    # dataset don't have a language code. The sounds of these languages still
    # get included in the combined inventory.


def test_get_phonological_inventories_na() -> None:
    """`get_phonological_inventories` shouldn't contain an NA inventory.

    If the Glottocode of a language isn't available, it should use the name of
    the language as key instead.
    """
    inventories = get_phonological_inventories()
    assert "NA" not in inventories

    assert "Djindewal" in inventories
    assert "ModernAramaic" in inventories


def test_get_phonological_inventories_glottocode_keys() -> None:
    """The keys of the return value of `get_phonological_inventories` should be
    Glottocodes, except for special keys.
    """
    special = {"*", "Djindewal", "ModernAramaic"}
    inventories = get_phonological_inventories()
    for glottocode in inventories:
        is_glottocode = re.match("[a-z]{4}[0-9]{4}", glottocode)
        if not is_glottocode:
            assert glottocode in special


def test_get_sounds() -> None:
    """`get_sounds(language)` should be the same as the keys in the sound
    inventory of the language.
    """
    # Test on a few languages, because it's slow.
    languages = ["*", "stan1293", "taga1270"]
    inventories = get_phonological_inventories()
    for language in languages:
        sounds = set(inventories[language])
        assert sounds == get_sounds(language)


def test_parse_allophones_with_pipe() -> None:
    """Segments with a pipe should be separated into multiple segments."""
    allophones = parse_allophones("a|b c|d e")
    assert allophones == set("abcde")


def test_diacritics() -> None:
    """Perform tests on diacritics that appear in the PHOIBLE inventory."""
    symbols: set[str] = set()
    inventory = set(get_phonological_inventories()["*"].keys())
    for sound in inventory:
        symbols.update(sound)

    for symbol in symbols:
        assert len(symbol) == 1

    # Voicelessness: only use ring below.
    # PHOIBLE actually uses both, but `get_phonological_inventories` should be
    # able to convert å into ḁ.
    combining_ring_above = "\u030a"
    combining_ring_below = "\u0325"
    assert combining_ring_above not in symbols
    assert combining_ring_below in symbols

    # Syllabicity: only use vertical line below.
    combining_vertical_line_below = "\u0329"
    combining_vertical_line_above = "\u030d"
    assert combining_vertical_line_above not in symbols
    assert combining_vertical_line_below in symbols

    # There should be no tie bars.
    combining_double_inverted_breve = "\u0361"
    combining_double_breve_below = "\u035c"
    assert combining_double_inverted_breve not in symbols
    assert combining_double_breve_below not in symbols


def test_no_invalid_segments_in_inventory(invalid_segments: list[str]) -> None:
    """There should be no invalid segments in the inventory (e.g. `tʂ`)."""
    inventory = set(get_phonological_inventories()["*"].keys())
    for segment in invalid_segments:
        assert segment not in inventory


def test_main(capsys: pytest.CaptureFixture[str]) -> None:
    """Output should be a CSV file with two columns."""
    main(Namespace())

    stdout, _ = capsys.readouterr()
    for line in stdout.splitlines():
        row = line.split(",")
        assert len(row) == 2


def test_symmetric_allophones() -> None:
    """If A is an allophone of B, then B is an allophone of A."""
    inventories = get_phonological_inventories()
    for inventory in inventories.values():
        for phoneme, allophones in inventory.items():
            for allophone in allophones:
                assert phoneme in inventory[allophone]
