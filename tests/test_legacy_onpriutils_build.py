import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_6_build


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


def make_base_character(level=1, build="", feats_taken=None):
    if feats_taken is None:
        feats_taken = []

    return {
        "name": "Test Hero",
        "level": level,
        "build": build,
        "base damage": "1d10",
        "feats taken": feats_taken,
    }


def test_pri_6_build_sets_strength_build_and_adds_focus_at_low_level(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_file = make_character_file(
        characters_dir,
        "test profile",
        make_base_character(level=1),
    )

    result = pri_6_build(
        charFolder=str(characters_dir) + "\\",
        message="strength",
        charFile=character_file,
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["build"] == "strength"
    assert saved_character["feats taken"] == ["focus"]
    assert "You have identified your character as a strength build" in result
    assert "Please ues [color=pink]!stats[/color] command" in result


def test_pri_6_build_sets_strength_build_without_focus_above_level_three(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_file = make_character_file(
        characters_dir,
        "test profile",
        make_base_character(level=4),
    )

    result = pri_6_build(
        charFolder=str(characters_dir) + "\\",
        message="strength",
        charFile=character_file,
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["build"] == "strength"
    assert saved_character["feats taken"] == []
    assert "You have identified your character as a strength build" in result


def test_pri_6_build_sets_dexterity_build_without_adding_focus(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_file = make_character_file(
        characters_dir,
        "test profile",
        make_base_character(level=1),
    )

    result = pri_6_build(
        charFolder=str(characters_dir) + "\\",
        message="dexterity",
        charFile=character_file,
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["build"] == "dexterity"
    assert saved_character["feats taken"] == []
    assert "You have identified your character as a dexterity build" in result


def test_pri_6_build_sets_constitution_build_without_adding_focus(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_file = make_character_file(
        characters_dir,
        "test profile",
        make_base_character(level=1),
    )

    result = pri_6_build(
        charFolder=str(characters_dir) + "\\",
        message="constitution",
        charFile=character_file,
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["build"] == "constitution"
    assert saved_character["feats taken"] == []
    assert "You have identified your character as a constitution build" in result


def test_pri_6_build_rejects_character_that_already_has_build(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_file = make_character_file(
        characters_dir,
        "test profile",
        make_base_character(
            level=1,
            build="strength",
            feats_taken=["focus"],
        ),
    )

    result = pri_6_build(
        charFolder=str(characters_dir) + "\\",
        message="dexterity",
        charFile=character_file,
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == "You already have selected a build."
    assert saved_character["build"] == "strength"
    assert saved_character["feats taken"] == ["focus"]