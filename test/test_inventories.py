# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test simphones.inventories."""
from simphones.inventories import get_phonological_inventories


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
