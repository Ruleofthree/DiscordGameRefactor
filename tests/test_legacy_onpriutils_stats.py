import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_6_stats


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


def make_base_character(
    build="strength",
    level=1,
    ap=15,
    strength=0,
    dexterity=0,
    constitution=0,
):
    return {
        "name": "Test Hero",
        "level": level,
        "build": build,
        "trait": "",
        "hp": 30,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 2,
        "damage": 2,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 1000,
        "strength": strength,
        "dexterity": dexterity,
        "constitution": constitution,
        "remaining feats": 0,
        "ap": ap,
        "apboost": False,
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


def test_pri_6_stats_rejects_missing_character_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character()

    result = pri_6_stats(
        message="!stat 6 4 5",
        character="missing profile",
        charData=char_data,
        charFile=characters_dir / "missing profile.json",
    )

    assert result == [
        "You don't even have a character created yet. Type !name <name> in the room. Where <name> is your character's actual name. (Example: !name Joe)"
    ]


def test_pri_6_stats_rejects_character_that_already_has_stats(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(
        build="strength",
        strength=6,
        dexterity=4,
        constitution=5,
    )

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 6 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == [
        "You have already set up your character's stats. If you want to change them, you will need to use the [color=pink]!respec[/color] command."
    ]
    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 5


def test_pri_6_stats_rejects_character_without_build(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(build="")

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 6 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == [
        "You need to pick a build path first. Please use the [color=pink]!build[/color] command."
    ]
    assert saved_character["strength"] == 0
    assert saved_character["dexterity"] == 0
    assert saved_character["constitution"] == 0


def test_pri_6_stats_rejects_total_that_does_not_equal_ap(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 5 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == [
        "Make sure total points used is no more or less than 15."
    ]
    assert saved_character["strength"] == 0
    assert saved_character["dexterity"] == 0
    assert saved_character["constitution"] == 0


def test_pri_6_stats_rejects_stat_above_level_one_cap(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 11 2 2",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == [
        "No one stat can be above 10 at this point in time. Please try again."
    ]
    assert saved_character["strength"] == 0
    assert saved_character["dexterity"] == 0
    assert saved_character["constitution"] == 0


def test_pri_6_stats_rejects_negative_stat(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat -1 8 8",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == [
        "Why would you even try to pick a negative stat? Please try again."
    ]
    assert saved_character["strength"] == 0
    assert saved_character["dexterity"] == 0
    assert saved_character["constitution"] == 0


def test_pri_6_stats_saves_strength_build_stats_and_bonuses(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(build="strength", level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 6 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 5
    assert saved_character["abhit"] == 3
    assert saved_character["abdamage"] == 3
    assert saved_character["abac"] == 2
    assert saved_character["abhp"] == 10
    assert saved_character["initiative"] == 2
    assert "Allocating the following:" in result[0]
    assert "Strength: 6" in result[0]
    assert "The above points have been placed on your character sheet." in result[1]


def test_pri_6_stats_saves_dexterity_build_stats_and_bonuses(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(build="dexterity", level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 5 6 4",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 5
    assert saved_character["dexterity"] == 6
    assert saved_character["constitution"] == 4
    assert saved_character["abhit"] == 1
    assert saved_character["abdamage"] == 1
    assert saved_character["abac"] == 3
    assert saved_character["abhp"] == 10
    assert saved_character["initiative"] == 3
    assert "Allocating the following:" in result[0]
    assert "Dexterity: 6" in result[0]
    assert "The above points have been placed on your character sheet." in result[1]


def test_pri_6_stats_saves_constitution_build_stats_and_bonuses(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(build="constitution", level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    result = pri_6_stats(
        message="!stat 6 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 5
    assert saved_character["abhit"] == 2
    assert saved_character["abdamage"] == 2
    assert saved_character["abac"] == 2
    assert saved_character["abhp"] == 6
    assert saved_character["initiative"] == 2
    assert "Allocating the following:" in result[0]
    assert "Constitution: 5" in result[0]
    assert "The above points have been placed on your character sheet." in result[1]


def test_pri_6_stats_refreshes_saved_combat_totals_after_successful_strength_build_assignment(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(build="strength", level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    pri_6_stats(
        message="!stat 6 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 5
    assert saved_character["thp"] == 40
    assert saved_character["tac"] == 14
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 6
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_6_stats_rejected_total_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(build="strength", level=1, ap=15)

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    pri_6_stats(
        message="!stat 5 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 0
    assert saved_character["dexterity"] == 0
    assert saved_character["constitution"] == 0
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99


def test_pri_6_stats_already_assigned_stats_do_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    char_data = make_base_character(
        build="strength",
        strength=6,
        dexterity=4,
        constitution=5,
    )

    character_file = make_character_file(
        characters_dir,
        "test profile",
        char_data,
    )

    pri_6_stats(
        message="!stat 6 4 5",
        character="test profile",
        charData=char_data,
        charFile=character_file,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 6
    assert saved_character["dexterity"] == 4
    assert saved_character["constitution"] == 5
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99
