# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Extract per-language phonological inventories from the PHOIBLE dataset."""

from csv import reader
from itertools import permutations
from pathlib import Path
import typing as t

from simphones.normalize import normalize_ipa


Phone: t.TypeAlias = str
AllophoneSet: t.TypeAlias = set[Phone]
Inventory: t.TypeAlias = dict[Phone, AllophoneSet]
LanguageCode: t.TypeAlias = str
InventoryDataset: t.TypeAlias = dict[LanguageCode, Inventory]


def get_phonological_inventories() -> InventoryDataset:
    """Get phonological inventories from the PHOIBLE dataset.

    The keys of the returned dictionary are ISO 639-3 language codes or "*".
    The "*" inventory combines the inventories of every language.
    """
    phoible = Path(__file__).with_name("phoible.csv")

    inventories: InventoryDataset = {}
    with open(phoible, encoding="utf-8") as file:
        rows = reader(file)
        next(rows)  # Drop the header.

        for row in rows:
            code = row[2]
            phoneme = normalize_ipa(row[6])
            allophones = parse_allophones(row[7])

            # Update combined inventory.
            combined_inventory = inventories.setdefault("*", {})
            update_inventory(combined_inventory, phoneme, allophones)

            # Update language inventory.
            assert code != ""
            if code not in ("NA", "mis"):
                language_inventory = inventories.setdefault(code, {})
                update_inventory(language_inventory, phoneme, allophones)
    return inventories


def parse_allophones(text: str) -> set[Phone]:
    """Parse space-separated list of allophones.

    Returns a set of allophones, or an empty set if the input is "NA".
    """
    if text in ("", "NA"):
        return set()

    allophones = set()
    for allophone in text.split():
        if (
            "<" in allophone or ">" in allophone or "⟨" in allophone
            or "⟩" in allophone
        ):
            # Angled brackets contain graphemes, not phonemes.
            continue
        allophones.add(normalize_ipa(allophone))
    return allophones


def update_inventory(
    inventory: Inventory,
    phoneme: Phone,
    allophones: AllophoneSet,
) -> None:
    """Update language inventory to include new phoneme-allophones information.

    Consider the phoneme and its allophones to be pairwise allophones.
    """
    phones = [phoneme, *allophones]
    for phone in phones:
        inventory.setdefault(phone, {phone})

    for phone, allophone in permutations(phones, 2):
        inventory[phone].add(allophone)


__all__ = ["get_phonological_inventories"]
