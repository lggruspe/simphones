# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Some pytest stuff."""

from pathlib import Path

import pytest


@pytest.fixture
def invalid_segments() -> list[str]:
    """Invalid segments in PHOIBLE.

    Future updates to PHOIBLE might fix these segments.
    When that happens, make sure to update the list of invalid segments here.
    """
    # See https://github.com/phoible/dev/issues/368
    return ["tʂ", "tʂʼ", "tʃː"]


@pytest.fixture
def phoible() -> Path:
    """Return path to `phoible.csv`."""
    return Path(__file__).parent.parent / "simphones" / "phoible.csv"
