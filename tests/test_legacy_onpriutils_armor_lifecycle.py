import json
import sys
from pathlib import Path

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
        "armor": {
            "armor1": ["str1", 500],
            "armor2": "n/a",
            "armor3": "n/a",
        },
        "equip": "",
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