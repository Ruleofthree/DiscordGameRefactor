import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_9_wholevel


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


def test_pri_9_wholevel_lists_profiles_at_requested_level(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_player_database(
        characters_dir,
        {
            "Alice Character": "alice",
            "Bob Character": "bob",
            "Cara Character": "cara",
        },
    )

    write_character(characters_dir, "alice", 3)
    write_character(characters_dir, "bob", 5)
    write_character(characters_dir, "cara", 3)

    result = pri_9_wholevel("tester", "!wholevel 3")

    assert result == [
        "Level 3 characters:",
        "\nalice\ncara",
    ]


def test_pri_9_wholevel_lists_single_matching_profile(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_player_database(
        characters_dir,
        {
            "Alice Character": "alice",
            "Bob Character": "bob",
        },
    )

    write_character(characters_dir, "alice", 1)
    write_character(characters_dir, "bob", 2)

    result = pri_9_wholevel("tester", "!wholevel 2")

    assert result == [
        "Level 2 characters:",
        "\nbob",
    ]


def test_pri_9_wholevel_returns_empty_second_message_when_no_profiles_match(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_player_database(
        characters_dir,
        {
            "Alice Character": "alice",
            "Bob Character": "bob",
        },
    )

    write_character(characters_dir, "alice", 1)
    write_character(characters_dir, "bob", 2)

    result = pri_9_wholevel("tester", "!wholevel 9")

    assert result == [
        "Level 9 characters:",
        "\n",
    ]