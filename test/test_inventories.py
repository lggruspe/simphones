# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test simphones.inventories."""
from simphones.inventories import (
    get_phonological_inventories,
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
