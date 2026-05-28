import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

import onPRIUtils


def test_pri_potion_shop_lists_delegates_to_repository(monkeypatch):
    expected = (
        ["hp5", "hp10"],
        ["hp15"],
        ["hp25"],
        ["damage5"],
        ["relic"],
    )

    monkeypatch.setattr(
        onPRIUtils,
        "get_potion_shop_lists",
        lambda: expected,
    )

    assert onPRIUtils.pri_potion_shop_lists() == expected


def test_pri_armor_shop_lists_delegates_to_repository(monkeypatch):
    expected = (
        ["str1"],
        ["str3"],
        ["str5"],
        ["init1"],
        ["init3"],
        ["init5"],
        ["damage1"],
        ["damage3"],
        ["damage5"],
    )

    monkeypatch.setattr(
        onPRIUtils,
        "get_armor_shop_lists",
        lambda: expected,
    )

    assert onPRIUtils.pri_armor_shop_lists() == expected