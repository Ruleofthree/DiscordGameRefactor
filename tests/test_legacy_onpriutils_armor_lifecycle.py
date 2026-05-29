from pathlib import Path
from onPRIUtils import pri_10_namearmor, pri_6_equip, pri_8_unequip

import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onPRIUtils import pri_10_namearmor


def write_character(characters_dir, profile_name, data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(json.dumps(data), encoding="utf-8")
    return character_file


def make_character(**overrides):
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
        "feats taken": [],
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
        "blur": 0,
        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traithp": 0,
        "traitregen": 0,
        "cursed": 0,
        "status": "",
        "statuscounter": 0,
        "fight": 0,
        "armor": {
            "armor1": ["str1", 500],
            "armor2": "n/a",
            "armor3": "n/a",
        },
        "equip": "",
        "armorhit": 0,
        "armordamage": 0,
        "armorac": 0,
        "armorhp": 0,
        "armordr": 0,
        "armorinitiative": 0,
        "armorstrength": 0,
        "armordexterity": 0,
        "armorconstitution": 0,
        "armorblur": 0,
        "traitdr": 0,
        "regeneration": 0,
        "initiative": 0,
    }
    data.update(overrides)
    return data


def test_pri_10_namearmor_rejects_missing_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    msg = pri_10_namearmor(
        "missingplayer",
        "new armor",
        "armor1",
        str(characters_dir) + "/",
    )

    assert msg == "You don't have a character made to use this command."


def test_pri_10_namearmor_rejects_armor_not_in_inventory(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "playerone", make_character())

    msg = pri_10_namearmor(
        "playerone",
        "new armor",
        "not owned",
        str(characters_dir) + "/",
    )

    assert msg == (
        "not owned is not within your inventory to rename. "
        "Please check you are typing armor name correctly, then try this command again"
    )


def test_pri_10_namearmor_rejects_duplicate_new_name(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "playerone",
        make_character(
            armor={
                "armor1": ["str1", 500],
                "duplicate": ["dex1", 500],
                "armor3": "n/a",
            }
        ),
    )

    msg = pri_10_namearmor(
        "playerone",
        "duplicate",
        "armor1",
        str(characters_dir) + "/",
    )

    assert msg == (
        "You already have a piece of armor named duplicate. "
        "Please use a new name, and try this command again"
    )


def test_pri_10_namearmor_rejects_equipped_armor(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "playerone",
        make_character(equip="armor1"),
    )

    msg = pri_10_namearmor(
        "playerone",
        "renamed armor",
        "armor1",
        str(characters_dir) + "/",
    )

    assert msg == "You need to unequip the armor first, before using this command."


def test_pri_10_namearmor_renames_unequipped_armor_and_preserves_value(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "playerone", make_character())

    msg = pri_10_namearmor(
        "playerone",
        "renamed armor",
        "armor1",
        str(characters_dir) + "/",
    )

    assert msg == "Test Hero renamed armor1 to renamed armor."

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert "armor1" not in updated["armor"]
    assert updated["armor"]["renamed armor"] == ["str1", 500]
    assert updated["armor"]["armor2"] == "n/a"
    assert updated["armor"]["armor3"] == "n/a"


def write_armor_file(tmp_path):
    armor_data = [
        {
            "cat1": {
                "common": {
                    "str1": [500, 1],
                    "dex1": [500, 1],
                    "con1": [500, 1],
                },
                "uncommon": {
                    "str3": [3000, 3],
                    "dex3": [3000, 3],
                    "con3": [3000, 3],
                },
                "rare": {
                    "str5": [7000, 5],
                    "dex5": [7000, 5],
                    "con5": [7000, 5],
                },
            },
            "cat2": {
                "common": {
                    "ac1": [2000, 1],
                    "hp10": [1000, 10],
                    "dr2": [5000, 2],
                    "init2": [750, 2],
                },
                "uncommon": {
                    "ac3": [6000, 3],
                    "hp15": [1500, 15],
                    "dr3": [7500, 3],
                    "init4": [3000, 4],
                },
                "rare": {
                    "ac5": [10000, 5],
                    "hp25": [2500, 25],
                    "init5": [4500, 5],
                },
            },
            "cat3": {
                "common": {
                    "hit2": [3000, 2],
                    "damage2": [3000, 2],
                    "blur1": [5000, 1],
                },
                "uncommon": {
                    "hit4": [6000, 4],
                    "damage4": [6000, 4],
                    "blur3": [12500, 3],
                },
                "rare": {
                    "hit5": [7500, 5],
                    "damage5": [7500, 5],
                    "blur5": [25000, 5],
                },
            },
            "armorlist": {},
        }
    ]

    armor_file = tmp_path / "armor.json"
    armor_file.write_text(json.dumps(armor_data), encoding="utf-8")
    return armor_file


def test_pri_6_equip_rejects_missing_character(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_armor_file(tmp_path)
    monkeypatch.chdir(tmp_path)

    msg = pri_6_equip(
        "missingplayer",
        "armor1",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "You don't have a character made to use this command."


def test_pri_6_equip_rejects_equipping_during_fight_and_preserves_existing_bonuses(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_armor_file(tmp_path)
    monkeypatch.chdir(tmp_path)

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
        ),
    )

    msg = pri_6_equip(
        "playerone",
        "armor2",
        str(characters_dir) + "/",
        1,
    )

    assert msg == "A fight is currently taking place...please wait until it is concluded."

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == "armor1"
    assert updated["armorstrength"] == 5
    assert updated["armorhit"] == 4
    assert updated["armordamage"] == 3
    assert updated["armorac"] == 2
    assert updated["armorhp"] == 10
    assert updated["armordr"] == 1
    assert updated["armorinitiative"] == 6
    assert updated["armordexterity"] == 7
    assert updated["armorconstitution"] == 8
    assert updated["armorblur"] == 9


def test_pri_6_equip_invalid_armor_name_clears_existing_armor_bonuses(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_armor_file(tmp_path)
    monkeypatch.chdir(tmp_path)

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
        ),
    )

    msg = pri_6_equip(
        "playerone",
        "not owned",
        str(characters_dir) + "/",
        0,
    )

    assert msg == (
        "not owned doesn't exist in your inventory. Make sure you are typing "
        "the armor name correctly when using this command"
    )

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == "armor1"
    assert updated["armorstrength"] == 0
    assert updated["armorhit"] == 0
    assert updated["armordamage"] == 0
    assert updated["armorac"] == 0
    assert updated["armorhp"] == 0
    assert updated["armordr"] == 0
    assert updated["armorinitiative"] == 0
    assert updated["armordexterity"] == 0
    assert updated["armorconstitution"] == 0
    assert updated["armorblur"] == 0


def test_pri_6_equip_applies_single_stat_armor_bonus(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_armor_file(tmp_path)
    monkeypatch.chdir(tmp_path)

    write_character(characters_dir, "playerone", make_character())

    msg = pri_6_equip(
        "playerone",
        "armor1",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "Test Hero has equipped armor1"

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == "armor1"
    assert updated["armorstrength"] == 1
    assert updated["armorhit"] == 0
    assert updated["armordamage"] == 0
    assert updated["armorac"] == 0
    assert updated["armorhp"] == 0
    assert updated["armordr"] == 0
    assert updated["armorinitiative"] == 0
    assert updated["armordexterity"] == 0
    assert updated["armorconstitution"] == 0
    assert updated["armorblur"] == 0


def test_pri_6_equip_applies_multi_stat_armor_bonus(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_armor_file(tmp_path)
    monkeypatch.chdir(tmp_path)

    write_character(
        characters_dir,
        "playerone",
        make_character(
            armor={
                "armor1": ["str3", "hp15", "hit4", 12000],
                "armor2": "n/a",
                "armor3": "n/a",
            }
        ),
    )

    msg = pri_6_equip(
        "playerone",
        "armor1",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "Test Hero has equipped armor1"

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == "armor1"
    assert updated["armorstrength"] == 3
    assert updated["armorhp"] == 15
    assert updated["armorhit"] == 4
    assert updated["armordamage"] == 0
    assert updated["armorac"] == 0
    assert updated["armordr"] == 0
    assert updated["armorinitiative"] == 0
    assert updated["armordexterity"] == 0
    assert updated["armorconstitution"] == 0
    assert updated["armorblur"] == 0


def test_pri_8_unequip_rejects_missing_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    msg = pri_8_unequip(
        "missingplayer",
        "armor1",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "You don't have a character made to use this command."


def test_pri_8_unequip_rejects_unequipping_during_fight_and_preserves_existing_bonuses(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
        ),
    )

    msg = pri_8_unequip(
        "playerone",
        "armor1",
        str(characters_dir) + "/",
        1,
    )

    assert msg == "A fight is currently taking place...please wait until it is concluded."

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == "armor1"
    assert updated["armorstrength"] == 5
    assert updated["armorhit"] == 4
    assert updated["armordamage"] == 3
    assert updated["armorac"] == 2
    assert updated["armorhp"] == 10
    assert updated["armordr"] == 1
    assert updated["armorinitiative"] == 6
    assert updated["armordexterity"] == 7
    assert updated["armorconstitution"] == 8
    assert updated["armorblur"] == 9


def test_pri_8_unequip_clears_equipped_armor_and_all_armor_bonuses(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
        ),
    )

    msg = pri_8_unequip(
        "playerone",
        "armor1",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "Test Hero has unequipped armor1"

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == ""
    assert updated["armorstrength"] == 0
    assert updated["armorhit"] == 0
    assert updated["armordamage"] == 0
    assert updated["armorac"] == 0
    assert updated["armorhp"] == 0
    assert updated["armordr"] == 0
    assert updated["armorinitiative"] == 0
    assert updated["armordexterity"] == 0
    assert updated["armorconstitution"] == 0
    assert updated["armorblur"] == 0


def test_pri_8_unequip_refreshes_saved_combat_totals_after_successful_armor_unequip(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
            thp=1,
            tac=1,
            tdr=1,
            thit=1,
            tdamage=1,
            initiative=1,
            regeneration=99,
        ),
    )

    msg = pri_8_unequip(
        "playerone",
        "armor1",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "Test Hero has unequipped armor1"

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))

    assert updated["equip"] == ""
    assert updated["armorstrength"] == 0
    assert updated["armorhit"] == 0
    assert updated["armordamage"] == 0
    assert updated["armorac"] == 0
    assert updated["armorhp"] == 0
    assert updated["armordr"] == 0
    assert updated["armorinitiative"] == 0
    assert updated["armordexterity"] == 0
    assert updated["armorconstitution"] == 0
    assert updated["armorblur"] == 0

    assert updated["thp"] == 40
    assert updated["tac"] == 14
    assert updated["tdr"] == 0
    assert updated["thit"] == 5
    assert updated["tdamage"] == 6
    assert updated["initiative"] == 2
    assert updated["regeneration"] == 0


def test_pri_8_unequip_during_combat_does_not_refresh_stale_combat_totals(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
            thp=1,
            tac=1,
            tdr=1,
            thit=1,
            tdamage=1,
            initiative=1,
            regeneration=99,
        ),
    )

    msg = pri_8_unequip(
        "playerone",
        "armor1",
        str(characters_dir) + "/",
        1,
    )

    assert msg == "A fight is currently taking place...please wait until it is concluded."

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))

    assert updated["equip"] == "armor1"
    assert updated["armorstrength"] == 5
    assert updated["armorhit"] == 4
    assert updated["armordamage"] == 3
    assert updated["armorac"] == 2
    assert updated["armorhp"] == 10
    assert updated["armordr"] == 1
    assert updated["armorinitiative"] == 6
    assert updated["armordexterity"] == 7
    assert updated["armorconstitution"] == 8
    assert updated["armorblur"] == 9

    assert updated["thp"] == 1
    assert updated["tac"] == 1
    assert updated["tdr"] == 1
    assert updated["thit"] == 1
    assert updated["tdamage"] == 1
    assert updated["initiative"] == 1
    assert updated["regeneration"] == 99


def test_pri_8_unequip_does_not_require_named_armor_to_exist(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "playerone",
        make_character(
            equip="armor1",
            armorstrength=5,
            armorhit=4,
            armordamage=3,
            armorac=2,
            armorhp=10,
            armordr=1,
            armorinitiative=6,
            armordexterity=7,
            armorconstitution=8,
            armorblur=9,
        ),
    )

    msg = pri_8_unequip(
        "playerone",
        "not owned",
        str(characters_dir) + "/",
        0,
    )

    assert msg == "Test Hero has unequipped not owned"

    updated = json.loads((characters_dir / "playerone.json").read_text(encoding="utf-8"))
    assert updated["equip"] == ""
    assert updated["armorstrength"] == 0
    assert updated["armorhit"] == 0
    assert updated["armordamage"] == 0
    assert updated["armorac"] == 0
    assert updated["armorhp"] == 0
    assert updated["armordr"] == 0
    assert updated["armorinitiative"] == 0
    assert updated["armordexterity"] == 0
    assert updated["armorconstitution"] == 0
    assert updated["armorblur"] == 0