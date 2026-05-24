import json

from src.character_repository import list_characters_by_level


def write_character(characters_dir, profile_name, level):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(
            {
                "name": profile_name.title(),
                "level": level,
            }
        ),
        encoding="utf-8",
    )


def write_player_database(characters_dir, player_database):
    (characters_dir / "playerDatabase.json").write_text(
        json.dumps(player_database),
        encoding="utf-8",
    )


def test_list_characters_by_level_returns_all_matching_profiles(tmp_path):
    write_player_database(
        tmp_path,
        {
            "Alice Character": "alice",
            "Bob Character": "bob",
            "Cara Character": "cara",
        },
    )

    write_character(tmp_path, "alice", 3)
    write_character(tmp_path, "bob", 5)
    write_character(tmp_path, "cara", 3)

    result = list_characters_by_level(3, tmp_path)

    assert result == ["alice", "cara"]


def test_list_characters_by_level_returns_single_matching_profile(tmp_path):
    write_player_database(
        tmp_path,
        {
            "Alice Character": "alice",
            "Bob Character": "bob",
        },
    )

    write_character(tmp_path, "alice", 1)
    write_character(tmp_path, "bob", 2)

    result = list_characters_by_level(2, tmp_path)

    assert result == ["bob"]


def test_list_characters_by_level_returns_empty_list_when_no_profiles_match(tmp_path):
    write_player_database(
        tmp_path,
        {
            "Alice Character": "alice",
            "Bob Character": "bob",
        },
    )

    write_character(tmp_path, "alice", 1)
    write_character(tmp_path, "bob", 2)

    result = list_characters_by_level(9, tmp_path)

    assert result == []