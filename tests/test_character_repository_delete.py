import json

from src.character_repository import delete_character


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_delete_character_removes_character_file_and_database_entry(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_file = characters_dir / "test player.json"
    player_database_file = characters_dir / "playerDatabase.json"

    write_json(character_file, {"name": "Sir Test"})
    write_json(player_database_file, {"Sir Test": "test player"})

    msg = delete_character("Test Player", characters_dir)

    assert msg == "Sir Test has been erased."
    assert not character_file.exists()
    assert read_json(player_database_file) == {}


def test_delete_character_reports_missing_character_file(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    player_database_file = characters_dir / "playerDatabase.json"
    write_json(player_database_file, {})

    msg = delete_character("Missing Player", characters_dir)

    assert msg == "You don't have a character to delete."
    assert read_json(player_database_file) == {}


def test_delete_character_removes_database_entry_even_if_character_file_is_missing(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    player_database_file = characters_dir / "playerDatabase.json"
    write_json(player_database_file, {"Sir Test": "test player"})

    msg = delete_character("Test Player", characters_dir)

    assert msg == "You don't have a character to delete."
    assert read_json(player_database_file) == {}