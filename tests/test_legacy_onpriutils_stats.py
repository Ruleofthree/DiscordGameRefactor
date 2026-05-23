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
        "ap": ap,
        "reset": 3,
        "build": build,
        "level": level,
        "strength": strength,
        "dexterity": dexterity,
        "constitution": constitution,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "abhp": 0,
        "initiative": 0,
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