import json
import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onPRIUtils import pri_10_usepotion


COMMON_LIST = [
    "hp5",
    "hp10",
    "tstr1",
    "tdex1",
    "tcon1",
    "tstr2",
    "tdex2",
    "tcon2",
    "damage1",
    "damage2",
    "hit1",
    "hit2",
    "respec",
    "ac1",
]

UNCOMMON_LIST = [
    "hp15",
    "hp20",
    "tstr3",
    "tdex3",
    "tcon3",
    "tstr4",
    "tdex4",
    "tcon4",
    "damage3",
    "hit3",
    "ac2",
]

RARE_LIST = [
    "hp25",
    "tstr5",
    "tdex5",
    "tcon5",
    "damage4",
    "hit4",
    "ac3",
    "str1",
    "dex1",
    "con1",
    "str2",
    "dex2",
    "con2",
    "regen1",
    "blur1",
]

VRARE_LIST = [
    "damage5",
    "hit5",
    "str3",
    "dex3",
    "con3",
    "str4",
    "dex4",
    "con4",
    "blur3",
    "regen2",
    "ac4",
]

RELIC_LIST = [
    "str5",
    "dex5",
    "blur5",
    "con5",
    "ac5",
    "regen3",
    "stimulant",
]


def write_potions_file(tmp_path):
    potions_data = [
        {
            "common": {
                "hit1": [500, "increasing hit chance by 1 for duration of fight", 1, "+1 to hit"],
                "respec": [250, "allows to respec character", 1, "allows to respec character"],
                "hp5": [150, "increasing hp by 5 for duration of fight", 5, "+5 hit points"],
                "tstr1": [250, "increasing strength by 1 for duration of fight", 1, "+1 strength"],
                "tdex1": [250, "increasing dexterity by 1 for duration of fight", 1, "+1 dexterity"],
                "tcon1": [250, "increasing constitution by 1 for duration of fight", 1, "+1 constitution"],
                "damage1": [500, "increasing damage by 1 for duration of fight", 1, "+1 to damage"],
                "ac1": [500, "increasing armor class by 1 for duration of fight", 1, "+1 to armor class"],
            },
            "uncommon": {},
            "rare": {
                "str1": [10000, "permanently increases strength by 1", 1],
                "str2": [
                    15000,
                    "permanently increases strength by 1 (cannot be used unless player has used a strength 1 potion)",
                    2,
                ],
                "regen1": [500, "grants +1 regeneration for duration of fight", 1, "+1 to regeneration"],
                "blur1": [80, "gives 1% chance to negate opponent's damage", 1, "1% chance to avoid damage"],
            },
            "vrare": {},
            "relic": {
                "stimulant": [
                    50000,
                    "Allows one to learn a new feat they meet requirements for",
                    1,
                    "Allows one to learn a new feat they meet requirements for",
                ],
            },
            "shoplist": [],
        }
    ]

    (tmp_path / "potions.json").write_text(
        json.dumps(potions_data, indent=2),
        encoding="utf-8",
    )


def base_character(**overrides):
    character = {
        "name": "Tester",
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
        "reset": 3,
        "remaining feats": 2,
        "total feats": 2,
        "traitdr": 0,
        "armordr": 0,
        "regeneration": 0,
    }
    character.update(overrides)
    return character


def write_character(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data, indent=2),
        encoding="utf-8",
    )
    return character_file


def read_character(characters_dir, profile_name):
    return json.loads((characters_dir / f"{profile_name}.json").read_text(encoding="utf-8"))


def call_usepotion(profile_name, potion, characters_dir):
    return pri_10_usepotion(
        profile_name,
        potion,
        COMMON_LIST,
        UNCOMMON_LIST,
        RARE_LIST,
        VRARE_LIST,
        RELIC_LIST,
        str(characters_dir) + os.sep,
    )


def test_pri_10_usepotion_returns_message_when_character_file_is_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    msg = call_usepotion("tester", "hit1", characters_dir)

    assert msg == "You don't have a character made to use these potions."


def test_pri_10_usepotion_returns_message_for_unknown_potion_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["hit1"]))

    msg = call_usepotion("tester", "notapotion", characters_dir)

    assert msg == "You do not have a potion of notapotion"
    updated = read_character(characters_dir, "tester")
    assert updated["potions"] == ["hit1"]


def test_pri_10_usepotion_applies_temporary_hit_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["hit1"]))

    msg = call_usepotion("tester", "hit1", characters_dir)

    assert (
            msg
            == "Tester drank a hit1 potion, [color=red]increasing hit chance by 1 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potionhit"] == 1
    assert updated["potioneffect"] == "increasing hit chance by 1 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_damage_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["damage1"]))

    msg = call_usepotion("tester", "damage1", characters_dir)

    assert (
        msg
        == "Testerdrank a damage1 potion, [color=red]increasing damage by 1 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potiondamage"] == 1
    assert updated["potioneffect"] == "increasing damage by 1 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_ac_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["ac1"]))

    msg = call_usepotion("tester", "ac1", characters_dir)

    assert (
        msg
        == "Tester drank a ac1 potion, [color=red]increasing armor class by 1 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potionac"] == 1
    assert updated["potioneffect"] == "increasing armor class by 1 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_strength_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["tstr1"]))

    msg = call_usepotion("tester", "tstr1", characters_dir)

    assert (
        msg
        == "Tester drank a tstr1 potion, [color=red]increasing strength by 1 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potionstr"] == 1
    assert updated["potioneffect"] == "increasing strength by 1 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_dexterity_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["tdex1"]))

    msg = call_usepotion("tester", "tdex1", characters_dir)

    assert (
        msg
        == "Tester drank a tdex1 potion, [color=red]increasing dexterity by 1 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potiondex"] == 1
    assert updated["potioneffect"] == "increasing dexterity by 1 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_constitution_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["tcon1"]))

    msg = call_usepotion("tester", "tcon1", characters_dir)

    assert (
        msg
        == "Tester drank a tcon1 potion, [color=red]increasing constitution by 1 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potioncon"] == 1
    assert updated["potioneffect"] == "increasing constitution by 1 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_hp_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["hp5"]))

    msg = call_usepotion("tester", "hp5", characters_dir)

    assert (
        msg
        == "Tester drank a hp5 potion, [color=red]increasing hp by 5 for duration of fight[/color] for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potionhp"] == 5
    assert updated["potioneffect"] == "increasing hp by 5 for duration of fight"
    assert updated["potions"] == []


def test_pri_10_usepotion_applies_temporary_blur_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "tester",
        base_character(
            potions=["blur1"],
            potionblur=2,
        ),
    )

    msg = call_usepotion("tester", "blur1", characters_dir)

    assert (
        msg
        == "Tester drank a blur1 potion, [color=red]gives 1% chance to negate opponent's damage for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potionblur"] == 3
    assert updated["potioneffect"] == "gives 1% chance to negate opponent's damage"
    assert updated["potions"] == []


def test_pri_10_usepotion_blocks_temporary_potion_when_potioneffect_is_active(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "tester",
        base_character(
            potions=["hit1"],
            potioneffect="existing effect",
        ),
    )

    msg = call_usepotion("tester", "hit1", characters_dir)

    assert msg == "You already have a potion in effect."
    updated = read_character(characters_dir, "tester")
    assert updated["potionhit"] == 0
    assert updated["potioneffect"] == "existing effect"
    assert updated["potions"] == ["hit1"]


def test_pri_10_usepotion_applies_valid_permanent_strength_progression(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["str1"], pstrength=0))

    msg = call_usepotion("tester", "str1", characters_dir)

    assert msg == "Tester drank a str1 potion, obtaining a permanent [color=red] +1 to strength[/color]"
    updated = read_character(characters_dir, "tester")
    assert updated["pstrength"] == 1
    assert updated["potions"] == []


def test_pri_10_usepotion_rejects_invalid_permanent_strength_progression(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["str2"], pstrength=0))

    msg = call_usepotion("tester", "str2", characters_dir)

    assert msg == "You can not drink this potion, as it is either too powerful or too weak to use right now."
    updated = read_character(characters_dir, "tester")
    assert updated["pstrength"] == 0
    assert updated["potions"] == ["str2"]


def test_pri_10_usepotion_respec_increments_reset_and_removes_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=["respec"], reset=3))

    msg = call_usepotion("tester", "respec", characters_dir)

    assert (
        msg
        == "Tester drank a respec potion. Allowing them a chance to change their feats, traits, and stat points."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["reset"] == 4
    assert updated["potions"] == []


def test_pri_10_usepotion_stimulant_adds_feat_slots_and_removes_potion(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "tester",
        base_character(
            potions=["stimulant"],
            **{
                "remaining feats": 2,
                "total feats": 2,
            },
        ),
    )

    msg = call_usepotion("tester", "stimulant", characters_dir)

    assert msg == "Tester drank a stimulant potion. Allowing them to learn a new feat they qualify for."
    updated = read_character(characters_dir, "tester")
    assert updated["remaining feats"] == 3
    assert updated["total feats"] == 3
    assert updated["potions"] == []


def test_pri_10_usepotion_regen_sets_effect_but_preserves_legacy_inventory_bug(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "tester",
        base_character(
            potions=["regen1"],
            traitdr=0,
            armordr=0,
            regeneration=0,
        ),
    )

    msg = call_usepotion("tester", "regen1", characters_dir)

    assert (
            msg
            == "Tester drank a regen1 potion, [color=red]grants +1 regeneration for duration of fight for next match."
    )
    updated = read_character(characters_dir, "tester")
    assert updated["potionregen"] == 1
    assert updated["potioneffect"] == "grants +1 regeneration for duration of fight"
    assert updated["potions"] == ["regen1"]


def test_pri_10_usepotion_regen_returns_no_benefit_when_all_blocking_fields_are_nonzero(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(
        characters_dir,
        "tester",
        base_character(
            potions=["regen1"],
            traitdr=1,
            armordr=1,
            regeneration=1,
        ),
    )

    msg = call_usepotion("tester", "regen1", characters_dir)

    assert msg == "Tester gains no benefit from this potion."
    updated = read_character(characters_dir, "tester")
    assert updated["potionregen"] == 0
    assert updated["potioneffect"] == ""
    assert updated["potions"] == ["regen1"]


def test_pri_10_usepotion_valid_potion_missing_from_inventory_raises_value_error(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_potions_file(tmp_path)
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "tester", base_character(potions=[]))

    with pytest.raises(ValueError):
        call_usepotion("tester", "hit1", characters_dir)