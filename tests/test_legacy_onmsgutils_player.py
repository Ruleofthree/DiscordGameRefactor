import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onMSGUtils import message_7_player


UNSPOILED_OOC = "ADH-8216a753c1ef08445052"
OTHER_CHANNEL = "ADH-00000000000000000000"


def write_character(char_folder, profile_name, character_data):
    character_path = char_folder / f"{profile_name}.json"
    character_path.write_text(
        json.dumps(character_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return character_path


def test_message_7_player_returns_score_for_existing_profile(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_character(
        char_folder,
        "their perfect doll",
        {
            "name": "Their Perfect Doll",
            "wins": 8,
            "losses": 2,
            "forfeits": 1,
        },
    )

    result = message_7_player(
        UNSPOILED_OOC,
        str(char_folder) + "/",
        UNSPOILED_OOC,
        "!player their perfect doll",
    )

    assert result == (
        "Their Perfect Doll's current win/loss score is: [color=pink]8 wins[/color], "
        "and [color=yellow]2 losses[/color]. ([color=red]80%[/color])"
        "They have also forfeited 1 times."
    )


def test_message_7_player_returns_zero_fight_message(tmp_path):
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

    result = message_7_player(
        UNSPOILED_OOC,
        str(char_folder) + "/",
        UNSPOILED_OOC,
        "!player their perfect doll",
    )

    assert result == (
        "Either Their Perfect Doll has a 0% win/loss ratio, or 100%. It all depends "
        "on how you justify a person that has never entered the arena yet."
    )


def test_message_7_player_returns_missing_character_message(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    result = message_7_player(
        UNSPOILED_OOC,
        str(char_folder) + "/",
        UNSPOILED_OOC,
        "!player missing player",
    )

    assert result == (
        "Either they don't have a character, or you fucked up typing. (type: !player <profile name>, "
        "[b]not[/b] character name. Example: !player their perfect doll"
    )


def test_message_7_player_rejects_wrong_channel(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    result = message_7_player(
        OTHER_CHANNEL,
        str(char_folder) + "/",
        UNSPOILED_OOC,
        "!player their perfect doll",
    )

    assert result == (
        "This Command can only be used in [session=Unspoiled Desire (Command and OoC Room)]"
        "adh-8216a753c1ef08445052[/session]"
    )