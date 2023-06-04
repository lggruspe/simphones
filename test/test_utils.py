# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Test simphones.utils."""
from pathlib import Path

from simphones.utils import save_as_json


def test_save_as_json_unicode(tmp_path: Path) -> None:
    """Unicode should not be escaped in the output file."""
    example = {
        ("á", "ä"): 0.1,
    }

    path = tmp_path/"out.json"
    save_as_json(path, example)

    text = path.read_text(encoding="utf-8")

    assert "á" in text
    assert "ä" in text
    assert "\\" not in text
