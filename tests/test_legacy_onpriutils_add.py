import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_4_add


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


def make_base_character(apboost=True):
    return {
        "name": "Test Hero",
        "level": 5,
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
        "constitution": 4,
        "remaining feats": 0,
        "ap": 15,
        "apboost": apboost,
        "regeneration": 99,
        "feats taken": [],
        "armor": {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a"},
        "equip": "",
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
        "armorhit": 0,
        "armordamage": 0,
        "armorac": 0,
        "armorhp": 0,
        "armordr": 0,
        "armorstrength": 0,
        "armordexterity": 0,
        "armorconstitution": 0,
        "armorblur": 0,
        "armorinitiative": 0,
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


def test_pri_4_add_adds_strength_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add strength",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 7
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_strength_abbreviation_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add str",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 7
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_dexterity_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add dexterity",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 5
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_dexterity_abbreviation_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add dex",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["dexterity"] == 5
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_constitution_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add constitution",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 5
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_constitution_abbreviation_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add con",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["constitution"] == 5
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_rejects_invalid_ability(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add wisdom",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is True
    assert result == [
        "You need to specify the ability you want to point the point to. Type '!add str' or '!add strength' for strength, and so on."
    ]


def test_pri_4_add_rejects_when_apboost_is_not_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=False),
    )

    result = pri_4_add(
        message="!add strength",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is False
    assert result == [
        "You do not have any more ability points to spend."
    ]


def test_pri_4_add_refreshes_saved_combat_totals_after_successful_strength_add(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    pri_4_add(
        message="!add strength",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 7
    assert saved_character["apboost"] is False
    assert saved_character["thp"] == 40
    assert saved_character["tac"] == 14
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 6
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_4_add_refreshes_saved_combat_totals_after_successful_dexterity_add(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    pri_4_add(
        message="!add dexterity",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["dexterity"] == 5
    assert saved_character["apboost"] is False
    assert saved_character["thp"] == 40
    assert saved_character["tac"] == 14
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 6
    assert saved_character["initiative"] == 2


def test_pri_4_add_refreshes_saved_combat_totals_after_successful_constitution_add(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    pri_4_add(
        message="!add constitution",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["constitution"] == 5
    assert saved_character["apboost"] is False
    assert saved_character["thp"] == 40
    assert saved_character["tac"] == 14
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 6
    assert saved_character["initiative"] == 2


def test_pri_4_add_invalid_ability_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    pri_4_add(
        message="!add wisdom",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is True
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99


def test_pri_4_add_without_apboost_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=False),
    )

    pri_4_add(
        message="!add strength",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is False
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99