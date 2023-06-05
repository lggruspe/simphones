# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Draw histogram of similarity scores."""

from argparse import ArgumentParser, Namespace
from pathlib import Path

import matplotlib.pyplot as plt     # type: ignore

from simphones.utils import read_from_csv


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-b",
        "--bins",
        dest="bins",
        default=10,
        type=int,
        help="number of bins in histogram (default: 10)",
    )
    parser.add_argument(
        "data",
        type=Path,
        help="path to simphones output CSV file",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    data = read_from_csv(args.data).values()

    plt.hist(data, bins=args.bins)
    plt.show()


if __name__ == "__main__":
    main(parse_args())
