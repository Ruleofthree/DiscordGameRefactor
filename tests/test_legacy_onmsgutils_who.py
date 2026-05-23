import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onMSGUtils import message_4_who


def make_character_file(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def make_player_database(characters_dir, database_data):
    database_file = characters_dir / "playerDatabase.json"
    database_file.write_text(
        json.dumps(database_data),
        encoding="utf-8",
    )
    return database_file


def test_message_4_who_returns_character_summary_for_existing_character(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_player_database(
        characters_dir,
        {
            "Test Hero": "test profile",
        },
    )

    make_character_file(
        characters_dir,
        "test profile",
        {
            "build": "strength",
            "wins": 3,
            "losses": 1,
            "forfeits": 2,
            "trait": "brawler",
            "level": 4,
        },
    )

    result = message_4_who(
        channel="ooc-room",
        charFolder=str(characters_dir),
        unspoiledBarOOC="ooc-room",
        message="!who test profile",
    )

    assert len(result) == 2
    assert "test profile's character name is: Test Hero" in result[0]
    assert "level: 4" in result[0]
    assert "strength" in result[0]
    assert "Test Hero's current win/loss score is" in result[1]
    assert "3 wins" in result[1]
    assert "1 losses" in result[1]
    assert "75%" in result[1]
    assert "forfeited 2 times" in result[1]


def test_message_4_who_marks_cursed_character(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_player_database(
        characters_dir,
        {
            "Cursed Hero": "cursed profile",
        },
    )

    make_character_file(
        characters_dir,
        "cursed profile",
        {
            "build": "dexterity",
            "wins": 0,
            "losses": 0,
            "forfeits": 0,
            "trait": "cursed",
            "level": 2,
        },
    )

    result = message_4_who(
        channel="ooc-room",
        charFolder=str(characters_dir),
        unspoiledBarOOC="ooc-room",
        message="!who cursed profile",
    )

    assert "[color=cyan]cursed[/color]" in result[0]


def test_message_4_who_handles_zero_fights(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_player_database(
        characters_dir,
        {
            "New Hero": "new profile",
        },
    )

    make_character_file(
        characters_dir,
        "new profile",
        {
            "build": "constitution",
            "wins": 0,
            "losses": 0,
            "forfeits": 0,
            "trait": "hearty",
            "level": 1,
        },
    )

    result = message_4_who(
        channel="ooc-room",
        charFolder=str(characters_dir),
        unspoiledBarOOC="ooc-room",
        message="!who new profile",
    )

    assert len(result) == 2
    assert "Either New Hero has a 0% win/loss ratio, or 100%." in result[1]


def test_message_4_who_handles_missing_character_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_player_database(
        characters_dir,
        {
            "Missing Hero": "missing profile",
        },
    )

    result = message_4_who(
        channel="ooc-room",
        charFolder=str(characters_dir),
        unspoiledBarOOC="ooc-room",
        message="!who missing profile",
    )

    assert len(result) == 1
    assert "missing profile isn't a valid name for a character sheet" in result[0]


def test_message_4_who_rejects_wrong_channel(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    result = message_4_who(
        channel="wrong-room",
        charFolder=str(characters_dir),
        unspoiledBarOOC="ooc-room",
        message="!who test profile",
    )

    assert len(result) == 1
    assert "This Command can only be used" in result[0]