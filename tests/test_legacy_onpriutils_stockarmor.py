import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


import onPRIUtils
from onPRIUtils import pri_11_stockarmor
from src.armor_repository import get_armor_dictionary


def make_armor_file(tmp_path, armor_dictionary):
    armor_file = tmp_path / "armor.json"
    armor_file.write_text(
        json.dumps(armor_dictionary),
        encoding="utf-8",
    )
    return armor_file


def load_armor_file(tmp_path):
    return json.loads((tmp_path / "armor.json").read_text(encoding="utf-8"))


def test_pri_11_stockarmor_stocks_twenty_cat_one_common_items(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    armor_dictionary = get_armor_dictionary()
    make_armor_file(tmp_path, armor_dictionary)
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)
    
    randint_values = iter([
                              41, 1,
                          ] * 20)

    monkeypatch.setattr("random.randint", lambda start, end: next(randint_values))
    monkeypatch.setattr("random.choice", lambda choices: choices[0])

    result = pri_11_stockarmor(
        ["str1"],
        ["str3"],
        ["str5"],
        ["ac1"],
        ["ac3"],
        ["ac5"],
        ["hit1"],
        ["hit3"],
        ["hit5"],
    )

    assert result == "Armor Shop has been stocked for the week."

    saved_armor = load_armor_file(tmp_path)

    expected_armor_list = {
        "armor" + str(number): ["str1"]
        for number in range(1, 21)
    }

    assert saved_armor[0]["armorlist"] == expected_armor_list


def test_pri_11_stockarmor_can_stock_three_attribute_items(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    armor_dictionary = get_armor_dictionary()
    make_armor_file(tmp_path, armor_dictionary)
    monkeypatch.setattr(onPRIUtils, "armorDictionary", armor_dictionary, raising=False)

    randint_values = iter([
        1, 1, 1, 1,
    ] * 20)

    monkeypatch.setattr("random.randint", lambda start, end: next(randint_values))
    monkeypatch.setattr("random.choice", lambda choices: choices[0])

    result = pri_11_stockarmor(
        ["str1"],
        ["str3"],
        ["str5"],
        ["ac1"],
        ["ac3"],
        ["ac5"],
        ["hit1"],
        ["hit3"],
        ["hit5"],
    )

    assert result == "Armor Shop has been stocked for the week."

    saved_armor = load_armor_file(tmp_path)

    expected_armor_list = {
        "armor" + str(number): ["str1", "ac1", "hit1"]
        for number in range(1, 21)
    }

    assert saved_armor[0]["armorlist"] == expected_armor_list