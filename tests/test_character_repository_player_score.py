import json

from src.character_repository import build_character_player_score_message


def write_character(char_folder, profile_name, character_data):
    character_path = char_folder / f"{profile_name}.json"
    character_path.write_text(
        json.dumps(character_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return character_path


def test_build_character_player_score_message_returns_score_with_ratio(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_character(
        char_folder,
        "their perfect doll",
        {
            "name": "Their Perfect Doll",
            "wins": 7,
            "losses": 3,
            "forfeits": 2,
        },
    )

    result = build_character_player_score_message(char_folder, "their perfect doll")

    assert result == (
        "Their Perfect Doll's current win/loss score is: [color=pink]7 wins[/color], "
        "and [color=yellow]3 losses[/color]. ([color=red]70%[/color])"
        "They have also forfeited 2 times."
    )


def test_build_character_player_score_message_handles_zero_fights(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_character(
        char_folder,
        "their perfect doll",
        {
            "name": "Their Perfect Doll",
            "wins": 0,
            "losses": 0,
            "forfeits": 0,
        },
    )

    result = build_character_player_score_message(char_folder, "their perfect doll")

    assert result == (
        "Either Their Perfect Doll has a 0% win/loss ratio, or 100%. It all depends "
        "on how you justify a person that has never entered the arena yet."
    )


def test_build_character_player_score_message_handles_missing_character(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    result = build_character_player_score_message(char_folder, "missing player")

    assert result == (
        "Either they don't have a character, or you fucked up typing. (type: !player <profile name>, "
        "[b]not[/b] character name. Example: !player their perfect doll"
    )


def test_build_character_player_score_message_lowercases_profile_name(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_character(
        char_folder,
        "their perfect doll",
        {
            "name": "Their Perfect Doll",
            "wins": 1,
            "losses": 1,
            "forfeits": 4,
        },
    )

    result = build_character_player_score_message(char_folder, "Their Perfect Doll")

    assert result == (
        "Their Perfect Doll's current win/loss score is: [color=pink]1 wins[/color], "
        "and [color=yellow]1 losses[/color]. ([color=red]50%[/color])"
        "They have also forfeited 4 times."
    )