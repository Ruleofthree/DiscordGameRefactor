from pathlib import Path
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_feats_json_loads():
    path = PROJECT_ROOT / "data" / "feats.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, list)
    assert len(data) > 0
    assert "power attack" in data[0]


def test_traits_json_loads():
    path = PROJECT_ROOT / "data" / "traits.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, list)
    assert len(data) > 0
    assert "regeneration" in data[0]


def test_potions_json_loads():
    path = PROJECT_ROOT / "data" / "potions.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, list)
    assert len(data) > 0
    assert "common" in data[0]


def test_armor_json_loads():
    path = PROJECT_ROOT / "data" / "armor.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, list)
    assert len(data) > 0
    assert "armorlist" in data[0]