import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_10_buypotion


def make_potions_file(tmp_path):
    potion_data = [
        {
            "shoplist": ["hp5", "damage1"],
            "common": {
                "hp5": [150, "increasing hp by 5 for duration of fight", 5],
            },
            "uncommon": {
                "damage1": [300, "increasing damage by 1 for duration of fight", 1],
            },
            "rare": {},
            "vrare": {},
            "relic": {},
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


def make_character_file(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def load_character_file(characters_dir, profile_name):
    character_file = characters_dir / f"{profile_name}.json"
    return json.loads(character_file.read_text(encoding="utf-8"))


def make_buyer(renown=500, potions=None):
    if potions is None:
        potions = []

    return {
        "name": "Test Hero",
        "renown": renown,
        "potions": potions,
    }


def test_pri_10_buypotion_buys_available_potion_and_updates_character_and_shop(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_potions_file(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_buyer(renown=500, potions=[]),
    )

    msg, buyer, potion = pri_10_buypotion(
        "tester",
        "hp5",
        str(characters_dir) + "/",
    )

    assert msg == "Test Hero has puchased a potion of hp5."
    assert buyer == "Test Hero"
    assert potion == "hp5"

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 350
    assert saved_character["potions"] == ["hp5"]

    potion_data = load_potions_file(tmp_path)
    assert potion_data[0]["shoplist"] == ["damage1"]


def test_pri_10_buypotion_rejects_potion_not_in_shop_without_changing_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_potions_file(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_buyer(renown=500, potions=[]),
    )

    msg, buyer, potion = pri_10_buypotion(
        "tester",
        "notforsale",
        str(characters_dir) + "/",
    )

    assert msg == "You can not buy that potion, as it is not being sold right now."
    assert buyer == "Test Hero"
    assert potion == "notforsale"

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 500
    assert saved_character["potions"] == []

    potion_data = load_potions_file(tmp_path)
    assert potion_data[0]["shoplist"] == ["hp5", "damage1"]


def test_pri_10_buypotion_rejects_when_buyer_lacks_renown(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_potions_file(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_buyer(renown=100, potions=[]),
    )

    msg, buyer, potion = pri_10_buypotion(
        "tester",
        "hp5",
        str(characters_dir) + "/",
    )

    assert msg == "You do not have enough renown to purchase this."
    assert buyer == "Test Hero"
    assert potion == "hp5"

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 100
    assert saved_character["potions"] == []

    potion_data = load_potions_file(tmp_path)
    assert potion_data[0]["shoplist"] == ["hp5", "damage1"]


def test_pri_10_buypotion_rejects_when_inventory_is_full(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_potions_file(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_buyer(
            renown=500,
            potions=["p1", "p2", "p3", "p4", "p5"],
        ),
    )

    msg, buyer, potion = pri_10_buypotion(
        "tester",
        "hp5",
        str(characters_dir) + "/",
    )

    assert msg == "You do not have enough inventory space to own more potions."
    assert buyer == "Test Hero"
    assert potion == "hp5"

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 500
    assert saved_character["potions"] == ["p1", "p2", "p3", "p4", "p5"]

    potion_data = load_potions_file(tmp_path)
    assert potion_data[0]["shoplist"] == ["hp5", "damage1"]