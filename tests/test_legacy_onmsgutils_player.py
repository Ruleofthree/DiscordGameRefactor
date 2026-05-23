import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onMSGUtils import message_7_player


def make_character_file(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def test_message_7_player_returns_score_for_existing_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        {
            "name": "Test Hero",
            "wins": 4,
            "losses": 1,
            "forfeits": 2,
        },
    )

    result = message_7_player(
        channel="ooc-room",
        charFolder=str(characters_dir) + "\\",
        unspoiledBarOOC="ooc-room",
        message="!player test profile",
    )

    assert "Test Hero's current win/loss score is" in result
    assert "4 wins" in result
    assert "1 losses" in result
    assert "80%" in result
    assert "forfeited 2 times" in result


def test_message_7_player_handles_zero_fights(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "new profile",
        {
            "name": "New Hero",
            "wins": 0,
            "losses": 0,
            "forfeits": 0,
        },
    )

    result = message_7_player(
        channel="ooc-room",
        charFolder=str(characters_dir) + "\\",
        unspoiledBarOOC="ooc-room",
        message="!player new profile",
    )

    assert "Either New Hero has a 0% win/loss ratio, or 100%." in result


def test_message_7_player_handles_missing_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    result = message_7_player(
        channel="ooc-room",
        charFolder=str(characters_dir) + "\\",
        unspoiledBarOOC="ooc-room",
        message="!player missing profile",
    )

    assert "Either they don't have a character" in result
    assert "type: !player <profile name>" in result


def test_message_7_player_rejects_wrong_channel(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    result = message_7_player(
        channel="wrong-room",
        charFolder=str(characters_dir) + "\\",
        unspoiledBarOOC="ooc-room",
        message="!player test profile",
    )

    assert "This Command can only be used" in result