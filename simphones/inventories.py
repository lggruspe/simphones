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


COMBINING_RING_ABOVE = "\u030a"     # like in å
COMBINING_RING_BELOW = "\u0325"     # like in ḁ


def substitute(phone: Phone) -> Phone:
    """Substitute some invalid glyphs inside phone segments."""
    substitutions = {
        "tʂ": "ʈʂ",
        "tʂʼ": "ʈʂʼ",
        "tʃː": "t̠ʃː",
        COMBINING_RING_ABOVE: COMBINING_RING_BELOW,
    }
    for key, value in substitutions.items():
        phone = phone.replace(key, value)
    return phone


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
            raw_phoneme = substitute(row[6])
            allophones = parse_allophones(row[7])

            if "|" in raw_phoneme:
                # Consider piped segments as allophones.
                raw_phoneme, *rest = raw_phoneme.split("|")
                allophones.update(parse_allophones(" ".join(rest)))
            phoneme = normalize_ipa(raw_phoneme)

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

    text = text.replace(COMBINING_RING_ABOVE, COMBINING_RING_BELOW)

    allophones: set[Phone] = set()
    for allophone in text.split():
        if (
            "<" in allophone or ">" in allophone or "⟨" in allophone
            or "⟩" in allophone
        ):
            # Angled brackets contain graphemes, not phonemes.
            continue

        # Some PHOIBLE segments have a vertical line, e.g. [t̪|t].
        # We split those into smaller segments.
        allophones.update(map(normalize_ipa, allophone.split("|")))
    return set(map(substitute, allophones))


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


def all_phones(language: LanguageCode = "*") -> set[Phone]:
    """Return set of all phones in the PHOIBLE data."""
    inventories = get_phonological_inventories()
    inventory = inventories.get(language, {})
    return set(inventory.keys())


def main() -> None:
    """Script entrypoint."""
    for phone in all_phones():
        print(phone)


if __name__ == "__main__":
    main()


__all__ = ["get_phonological_inventories"]
