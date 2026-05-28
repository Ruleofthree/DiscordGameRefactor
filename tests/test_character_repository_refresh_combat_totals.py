import json

from src.character_repository import (
    load_character,
    refresh_character_combat_totals,
)


def make_character_data():
    return {
        "name": "Refresh Hero",
        "level": 5,
        "build": "strength",
        "trait": "brawler",
        "hp": 20,
        "total feats": 3,
        "base damage": "1d10",
        "hit": 3,
        "damage": 4,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 1000,
        "strength": 8,
        "dexterity": 6,
        "constitution": 10,
        "remaining feats": 0,
        "ap": 15,
        "apboost": False,
        "regeneration": 99,
        "feats taken": ["focus"],
        "armor": {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a"},
        "equip": "",
        "hfeats taken": ["focus"],
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "forfeits": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 5,
        "feathit": 1,
        "featdamage": 1,
        "featac": 1,
        "thp": 1,
        "tac": 2,
        "thit": 3,
        "tdamage": 4,
        "tdr": 5,
        "dexfighter": 0,
        "renown": 0,
        "initiative": 6,
        "potions": [],
        "potioneffect": "",
        "potionhit": 0,
        "potiondamage": 0,
        "potionac": 0,
        "potionhp": 11,
        "potionblur": 0,
        "potionstr": 3,
        "potiondex": 3,
        "potioncon": 3,
        "potionregen": 3,
        "pstrength": 1,
        "pdexterity": 1,
        "pconstitution": 1,
        "armorhit": 2,
        "armordamage": 2,
        "armorac": 2,
        "armorhp": 7,
        "armordr": 4,
        "armorstrength": 2,
        "armordexterity": 2,
        "armorconstitution": 2,
        "armorblur": 0,
        "armorinitiative": 4,
        "blur": 0,
        "traithit": 3,
        "traitdamage": 3,
        "traitac": 3,
        "traitdr": 5,
        "traithp": 13,
        "traitregen": 2,
        "cursed": 0,
        "status": "",
        "statuscounter": 0,
        "fight": 0,
    }


def write_character(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return character_file


def test_refresh_character_combat_totals_updates_saved_combat_facing_fields(tmp_path):
    character_data = make_character_data()
    write_character(tmp_path, "refresh hero", character_data)

    refreshed_data = refresh_character_combat_totals("refresh hero", characters_dir=tmp_path)
    saved_data = load_character("refresh hero", characters_dir=tmp_path)

    expected_saved_totals = {
        "thp": 96,
        "tac": 24,
        "tdr": 9,
        "thit": 16,
        "tdamage": 19,
        "initiative": 10,
        "regeneration": 5,
    }

    for field, expected_value in expected_saved_totals.items():
        assert refreshed_data[field] == expected_value
        assert saved_data[field] == expected_value

    assert saved_data["name"] == "Refresh Hero"
    assert saved_data["build"] == "strength"


def test_refresh_character_combat_totals_normalizes_character_name_for_file_lookup(tmp_path):
    character_data = make_character_data()
    write_character(tmp_path, "refresh hero", character_data)

    refreshed_data = refresh_character_combat_totals("  Refresh Hero  ", characters_dir=tmp_path)
    saved_data = load_character("refresh hero", characters_dir=tmp_path)

    assert refreshed_data["thp"] == 96
    assert saved_data["thp"] == 96
    assert saved_data["initiative"] == 10
