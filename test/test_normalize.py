# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test simphones.normalize."""
from random import shuffle
from unicodedata import normalize

from simphones.normalize import modifiers, normalize_ipa


def test_normalize_ipa_on_basic_unicode() -> None:
    """The result should be similar to NFD normalization in simple cases."""
    example = "ä"
    output = normalize_ipa(example)

    assert example == normalize("NFC", example)
    assert example != normalize("NFD", example)

    assert output != normalize("NFC", example)
    assert output == normalize("NFD", example)


def test_normalize_ipa_sort_order() -> None:
    """Modifier symbols should be sorted according to PHOIBLE conventions."""
    keys = list(modifiers.keys())
    shuffle(keys)
    symbols = normalize_ipa("".join(keys))

    # This should be monotone.
    order = [modifiers[symbol] for symbol in symbols]
    for i in range(1, len(order)):
        assert order[i-1] <= order[i]
