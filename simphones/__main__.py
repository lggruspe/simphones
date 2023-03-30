# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Compute phone similarity from PHOIBLE allophone data."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

from simphones.inventories import get_phonological_inventories
from simphones.similarity import compute_similarity
from simphones.utils import save_as_csv


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(prog="simphones", description=__doc__)
    parser.add_argument(
        "output",
        type=Path,
        help="output CSV file",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    inventories = get_phonological_inventories()
    similarity = compute_similarity(inventories)
    save_as_csv(args.output, similarity)


if __name__ == "__main__":
    main(parse_args())
