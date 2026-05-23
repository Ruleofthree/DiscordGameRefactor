import json

import pytest

from src.character_repository import (
    character_exists,
    get_character_path,
    load_character,
    normalize_character_name,
    save_character,
)


def test_normalize_character_name_strips_and_lowercases_name():
    result = normalize_character_name("  Test Character  ")

    assert result == "test character"


def test_get_character_path_uses_lowercase_json_filename(tmp_path):
    result = get_character_path("Test Character", tmp_path)

    assert result == tmp_path / "test character.json"


def test_character_exists_returns_true_when_file_exists(tmp_path):
    character_file = tmp_path / "test character.json"
    character_file.write_text("{}", encoding="utf-8")

    result = character_exists("Test Character", tmp_path)

    assert result is True


def test_character_exists_returns_false_when_file_does_not_exist(tmp_path):
    result = character_exists("Missing Character", tmp_path)

    assert result is False


def test_save_character_writes_character_json_to_temp_directory(tmp_path):
    character_data = {
        "name": "Test Character",
        "level": 1,
        "renown": 25,
    }

    save_character("Test Character", character_data, tmp_path)

    character_file = tmp_path / "test character.json"
    assert character_file.is_file()

    saved_data = json.loads(character_file.read_text(encoding="utf-8"))
    assert saved_data == character_data


def test_load_character_reads_character_json_from_temp_directory(tmp_path):
    character_data = {
        "name": "Test Character",
        "level": 3,
        "currentxp": 150,
    }

    character_file = tmp_path / "test character.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )

    result = load_character("Test Character", tmp_path)

    assert result == character_data


def test_load_character_raises_file_not_found_for_missing_character(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_character("Missing Character", tmp_path)


def test_save_character_creates_character_directory_if_missing(tmp_path):
    characters_dir = tmp_path / "characters"
    character_data = {"name": "Test Character"}

    save_character("Test Character", character_data, characters_dir)

    assert (characters_dir / "test character.json").is_file()