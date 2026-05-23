import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_viewchar


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


def make_viewchar_character(build="strength"):
    return {
        "name": "Test Hero",
        "build": build,
        "trait": "brawler",
        "level": 1,
        "hp": 20,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 2,
        "damage": 3,
        "ac": 10,
        "renown": 100,
        "currentxp": 50,
        "nextlevel": 100,
        "strength": 6,
        "dexterity": 4,
        "constitution": 5,
        "remaining feats": 1,
        "feats taken": ["focus"],
        "hfeats taken": ["focus"],
        "ap": 15,
        "reset": 3,
        "wins": 2,
        "losses": 1,
        "forfeits": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "dexfighter": 0,
        "potioneffect": "",
        "potions": [],
        "potionstr": 0,
        "potiondex": 0,
        "potioncon": 0,
        "potionregen": 0,
        "pstrength": 0,
        "pdexterity": 0,
        "pconstitution": 0,
        "potionblur": 0,
        "potionhp": 0,
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        },
        "equip": "",
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
        "thp": 0,
        "tac": 0,
        "tdr": 0,
        "thit": 0,
        "tdamage": 0,
        "initiative": 0,
        "regeneration": 0,
    }


def test_pri_viewchar_returns_missing_character_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    result = pri_viewchar("missing profile")

    assert result == [
        "You don't even have a character created yet. Type !name <name> in the room. Where <name> is your character's actual name. (Example: !name Joe"
    ]


def test_pri_viewchar_displays_strength_character_and_updates_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_viewchar_character(build="strength"),
    )

    result = pri_viewchar("test profile")
    saved_character = load_character_file(characters_dir, "test profile")

    assert len(result) == 1
    assert "Test Hero's Character Sheet" in result[0]
    assert "Build:" in result[0]
    assert "[color=red]strength[/color]" in result[0]
    assert "𝚂𝚝𝚛𝚎𝚗𝚐𝚝𝚑" in result[0]
    assert "[color=red]6[/color]" in result[0]
    assert saved_character["thp"] == 30
    assert saved_character["tac"] == 14
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 7
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_viewchar_displays_dexterity_character_and_updates_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_viewchar_character(build="dexterity"),
    )

    result = pri_viewchar("test profile")
    saved_character = load_character_file(characters_dir, "test profile")

    assert len(result) == 1
    assert "Test Hero's Character Sheet" in result[0]
    assert "[color=red]dexterity[/color]" in result[0]
    assert saved_character["thp"] == 30
    assert saved_character["tac"] == 12
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 4
    assert saved_character["tdamage"] == 5
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_viewchar_displays_constitution_character_and_updates_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_viewchar_character(build="constitution"),
    )

    result = pri_viewchar("test profile")
    saved_character = load_character_file(characters_dir, "test profile")

    assert len(result) == 1
    assert "Test Hero's Character Sheet" in result[0]
    assert "[color=red]constitution[/color]" in result[0]
    assert saved_character["thp"] == 26
    assert saved_character["tac"] == 16
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 6
    assert saved_character["tdamage"] == 5
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0