import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_6_equip


def make_character_file(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(json.dumps(character_data), encoding="utf-8")
    return character_file


def load_character_file(characters_dir, profile_name):
    return json.loads((characters_dir / f"{profile_name}.json").read_text(encoding="utf-8"))


def make_armor_file(base_dir):
    armor_data = [
        {
            "cat1": {
                "common": {
                    "str1": [500, 1],
                    "str2": [1000, 2],
                    "dex2": [1000, 2],
                },
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {
                    "hp10": [1000, 10],
                    "ac2": [4000, 2],
                },
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {
                    "damage3": [4500, 3],
                    "hit4": [6000, 4],
                },
                "rare": {},
            },
            "armorlist": {},
        }
    ]

    (base_dir / "armor.json").write_text(json.dumps(armor_data), encoding="utf-8")


def make_base_character(**overrides):
    data = {
        "name": "Test Hero",
        "level": 1,
        "build": "strength",
        "trait": "",
        "hp": 30,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 2,
        "damage": 2,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 1000,
        "strength": 6,
        "dexterity": 4,
        "constitution": 5,
        "remaining feats": 2,
        "ap": 15,
        "apboost": False,
        "regeneration": 99,
        "feats taken": [],
        "armor": {
            "old armor": ["str1", 500],
            "new armor": ["str2", "hp10", "damage3", 500],
            "defense armor": ["dex2", "ac2", "hit4", 500],
        },
        "equip": "old armor",
        "hfeats taken": [],
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "forfeits": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "thp": 1,
        "tac": 1,
        "thit": 1,
        "tdamage": 1,
        "tdr": 1,
        "dexfighter": 0,
        "renown": 0,
        "initiative": 1,
        "potions": [],
        "potioneffect": "",
        "potionhit": 0,
        "potiondamage": 0,
        "potionac": 0,
        "potionhp": 0,
        "potionblur": 0,
        "potionstr": 0,
        "potiondex": 0,
        "potioncon": 0,
        "potionregen": 0,
        "pstrength": 0,
        "pdexterity": 0,
        "pconstitution": 0,
        "armorhit": 9,
        "armordamage": 9,
        "armorac": 9,
        "armorhp": 9,
        "armordr": 9,
        "armorstrength": 9,
        "armordexterity": 9,
        "armorconstitution": 9,
        "armorblur": 9,
        "armorinitiative": 9,
        "blur": 0,
        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traitdr": 0,
        "traithp": 0,
        "traitregen": 0,
        "cursed": 0,
        "status": "",
        "statuscounter": 0,
        "fight": 0,
    }
    data.update(overrides)
    return data


def test_pri_6_equip_refreshes_saved_combat_totals_after_successful_armor_equip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_armor_file(tmp_path)

    make_character_file(characters_dir, "test profile", make_base_character())

    result = pri_6_equip(
        character="test profile",
        armor="new armor",
        charFolder=str(characters_dir) + "/",
        game=0,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == "Test Hero has equipped new armor"
    assert saved_character["equip"] == "new armor"
    assert saved_character["armorstrength"] == 2
    assert saved_character["armorhp"] == 10
    assert saved_character["armordamage"] == 3
    assert saved_character["thp"] == 50
    assert saved_character["tac"] == 14
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 6
    assert saved_character["tdamage"] == 10
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_6_equip_invalid_armor_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_armor_file(tmp_path)

    make_character_file(characters_dir, "test profile", make_base_character())

    result = pri_6_equip(
        character="test profile",
        armor="missing armor",
        charFolder=str(characters_dir) + "/",
        game=0,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == (
        "missing armor doesn't exist in your inventory. Make sure you are typing the armor name correctly when using"
        " this command"
    )
    assert saved_character["equip"] == "old armor"
    assert saved_character["armorstrength"] == 0
    assert saved_character["armorhp"] == 0
    assert saved_character["armordamage"] == 0
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99


def test_pri_6_equip_during_combat_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_armor_file(tmp_path)

    make_character_file(characters_dir, "test profile", make_base_character())

    result = pri_6_equip(
        character="test profile",
        armor="new armor",
        charFolder=str(characters_dir) + "/",
        game=1,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == "A fight is currently taking place...please wait until it is concluded."
    assert saved_character["equip"] == "old armor"
    assert saved_character["armorstrength"] == 9
    assert saved_character["armorhp"] == 9
    assert saved_character["armordamage"] == 9
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99
