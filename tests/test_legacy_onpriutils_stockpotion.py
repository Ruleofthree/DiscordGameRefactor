import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_10_stockpotion


def make_potions_file(tmp_path):
    potion_data = [
        {
            "shoplist": ["old potion"],
            "common": {
                "common0": [10, "common zero", 0],
                "common1": [20, "common one", 1],
            },
            "uncommon": {
                "uncommon0": [30, "uncommon zero", 0],
                "uncommon1": [40, "uncommon one", 1],
            },
            "rare": {
                "rare0": [50, "rare zero", 0],
                "rare1": [60, "rare one", 1],
            },
            "vrare": {
                "vrare0": [70, "vrare zero", 0],
                "vrare1": [80, "vrare one", 1],
            },
            "relic": {
                "relic0": [90, "relic zero", 0],
                "relic1": [100, "relic one", 1],
            },
        }
    ]

    potion_file = tmp_path / "potions.json"
    potion_file.write_text(
        json.dumps(potion_data),
        encoding="utf-8",
    )
    return potion_file


def load_potions_file(tmp_path):
    return json.loads((tmp_path / "potions.json").read_text(encoding="utf-8"))


def test_pri_10_stockpotion_replaces_shoplist_with_twenty_common_potions(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_potions_file(tmp_path)

    monkeypatch.setattr("random.randint", lambda start, end: 1)

    msg, shop_string = pri_10_stockpotion(
        ["common0", "common1"],
        ["uncommon0", "uncommon1"],
        ["rare0", "rare1"],
        ["vrare0", "vrare1"],
        ["relic0", "relic1"],
    )

    expected_shop = ["common1"] * 20

    assert shop_string == ", ".join(expected_shop)
    assert msg == "Shop stocked for the week as follows: \n" + shop_string

    potion_data = load_potions_file(tmp_path)
    assert potion_data[0]["shoplist"] == expected_shop


def test_pri_10_stockpotion_can_stock_each_rarity_bucket(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_potions_file(tmp_path)

    rolls = iter([
        1, 1,
        51, 1,
        77, 1,
        90, 1,
        98, 1,
    ] * 4)

    monkeypatch.setattr("random.randint", lambda start, end: next(rolls))

    msg, shop_string = pri_10_stockpotion(
        ["common0", "common1"],
        ["uncommon0", "uncommon1"],
        ["rare0", "rare1"],
        ["vrare0", "vrare1"],
        ["relic0", "relic1"],
    )

    expected_shop = [
        "common1",
        "uncommon1",
        "rare1",
        "vrare1",
        "relic1",
    ] * 4

    assert shop_string == ", ".join(expected_shop)
    assert msg == "Shop stocked for the week as follows: \n" + shop_string

    potion_data = load_potions_file(tmp_path)
    assert potion_data[0]["shoplist"] == expected_shop