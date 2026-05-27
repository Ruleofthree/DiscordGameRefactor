import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


import onPRIUtils
from onPRIUtils import pri_10_armorshop
from src.armor_repository import get_armor_dictionary


def test_pri_10_armorshop_formats_single_attribute_armor(monkeypatch):
    armor_dictionary = get_armor_dictionary()
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)

    result = pri_10_armorshop([
        ["str1"],
    ])

    assert result == "Armor1 [color=red]['str1'][/color]: [color=yellow](500 renown)[/color]"


def test_pri_10_armorshop_formats_two_attribute_armor(monkeypatch):
    armor_dictionary = get_armor_dictionary()
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)

    result = pri_10_armorshop([
        ["dex2", "ac2"],
    ])

    assert result == "Armor1 [color=red]['dex2', 'ac2'][/color]: [color=yellow](5000 renown)[/color]"


def test_pri_10_armorshop_formats_three_attribute_armor(monkeypatch):
    armor_dictionary = get_armor_dictionary()
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)

    result = pri_10_armorshop([
        ["con4", "hp15", "hit4"],
    ])

    assert result == "Armor1 [color=red]['con4', 'hp15', 'hit4'][/color]: [color=yellow](12500 renown)[/color]"


def test_pri_10_armorshop_formats_sold_armor(monkeypatch):
    armor_dictionary = get_armor_dictionary()
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)

    result = pri_10_armorshop([
        "sold",
    ])

    assert result == "Armor1 [color=red]sold[/color]: [color=yellow](0 renown)[/color]"


def test_pri_10_armorshop_preserves_multiple_line_display(monkeypatch):
    armor_dictionary = get_armor_dictionary()
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)

    result = pri_10_armorshop([
        ["str1"],
        ["dex2", "ac2"],
        ["con4", "hp15", "hit4"],
        "sold",
    ])

    assert result == (
        "Armor1 [color=red]['str1'][/color]: [color=yellow](500 renown)[/color]\n"
        "Armor2 [color=red]['dex2', 'ac2'][/color]: [color=yellow](5000 renown)[/color]\n"
        "Armor3 [color=red]['con4', 'hp15', 'hit4'][/color]: [color=yellow](12500 renown)[/color]\n"
        "Armor4 [color=red]sold[/color]: [color=yellow](0 renown)[/color]"
    )


def test_pri_armorshop_loads_armor_data_and_returns_shop_display(monkeypatch):
    armor_data = [{"armorlist": {"armor1": ["str1"]}}]

    monkeypatch.setattr(
        onPRIUtils,
        "get_armor_dictionary",
        lambda: armor_data,
    )
    monkeypatch.setattr(
        onPRIUtils,
        "build_armor_shop_display",
        lambda loaded_items: "Armor1 [color=red]['str1'][/color]: [color=yellow](500 renown)[/color]",
    )

    result = onPRIUtils.pri_armorshop()

    assert result == "Armor1 [color=red]['str1'][/color]: [color=yellow](500 renown)[/color]"
