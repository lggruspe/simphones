# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Normalize IPA transcriptions according to the convention used by PHOIBLE."""

from unicodedata import normalize


# IPA modifiers and diacritics mapped to PHOIBLE sort order
modifiers = {
    # Place features
    "\u0334": 0,    # velarized/pharyngealized
    "\u033c": 1,    # linguolabial
    "\u032a": 2,    # dental
    "\u033a": 3,    # apical: u02fd; u1df9 (?)
    "\u033b": 4,    # laminal
    "\u031f": 5,    # advanced: u02d6; u1ac (?)
    "\u0320": 6,    # retracted: u02cd; u02d7

    # Manner features
    "\u0347": 7,    # non-sibilant
    "\u031d": 8,    # raised: u02d4
    "\u031e": 9,    # lowered: u02d5
    "\u0318": 10,   # advanced tongue root: uab6a
    "\u0319": 11,   # retracted tongue root: uab6b
    "\u0353": 12,   # frictionalized

    # Secondary articulations
    "\u0339": 13,   # more round: u02d2
    "\u031c": 14,   # less round: u02d3

    # Laryngeal settings
    "\u0330": 15,   # creaky: u02f7
    "\u0324": 16,   # breathy
    "\u032c": 17,   # voiced
    # "\u032c": 18,   # stiff
    "\u0325": 19,   # devoiced (below): u02f3
    "\u030a": 20,   # devoiced (above)
    "\u0348": 21,   # fortis
    "\u0349": 22,   # lenis

    # Length
    "\u0306": 23,   # short: u02d8 (?) ua67c (?)

    # Syllabicity
    "\u0329": 24,   # syllabic: u02cc
    "\u032f": 25,   # non-syllabic

    # Vowel quality modifications
    "\u0303": 26,   # nasalized: u007e (?) u02dc (?)
    "\u034a": 27,   # denasalized
    "\u0308": 28,   # centralized: u00a8
    "\u033d": 29,   # mid-centralized: u02df

    # Stop release
    "\u031a": 30,   # unreleased: u02fa

    # Spacing modifier letters
    "\u02de": 31,   # rhotic hook
    "\u207f": 31,   # nasal release
    "\u02e1": 31,   # lateral release
    "\u02b7": 31,   # labialized: u1ac7 (?) u032b (?)
    "\u02b2": 31,   # palatalized
    "\u1da3": 31,   # labial-palatalized
    "\u02e0": 31,   # velarized
    "\u02e4": 31,   # pharyngealized
    "\u02c0": 31,   # glottalized
    "\u1d4a": 31,   # schwa-like release
    "\u1d31": 31,   # epilaryngeal source
    "\u02b0": 31,   # aspirated
    "\u02b1": 31,   # breathy aspirated
    "\u02bc": 31,   # ejective
    "\u02d0": 31,   # long
    "\u02d1": 31,   # half long
}


def sort_order(modifier: str) -> int:
    """Modifier sort order."""
    return modifiers[modifier]


def normalize_ipa(transcription: str) -> str:
    """Normalize string according to the convention used by PHOIBLE."""
    result = ""
    segment = []
    for symbol in normalize("NFD", transcription):
        if symbol in modifiers:
            segment.append(symbol)
            continue

        segment.sort(key=sort_order)
        result += "".join(segment) + symbol
        segment.clear()

    if segment:
        segment.sort(key=sort_order)
        result += "".join(segment)
    return result


__all__ = ["modifiers", "normalize_ipa"]
