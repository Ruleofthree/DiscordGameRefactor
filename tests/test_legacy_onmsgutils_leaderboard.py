import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onMSGUtils import message_12_leaderboard


def write_character(characters_dir, profile_name, data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )


def base_character(name, wins=0, losses=0, level=1):
    return {
        "name": name,
        "wins": wins,
        "losses": losses,
        "level": level,
    }


def setup_leaderboard_characters(characters_dir):
    player_database = {
        "Alpha Character": "alpha",
        "Bravo Character": "bravo",
        "Charlie Character": "charlie",
        "Delta Character": "delta",
        "Echo Character": "echo",
    }

    (characters_dir / "playerDatabase.json").write_text(
        json.dumps(player_database),
        encoding="utf-8",
    )

    write_character(characters_dir, "alpha", base_character("Alpha Character", wins=5, losses=2, level=3))
    write_character(characters_dir, "bravo", base_character("Bravo Character", wins=1, losses=8, level=4))
    write_character(characters_dir, "charlie", base_character("Charlie Character", wins=10, losses=0, level=5))
    write_character(characters_dir, "delta", base_character("Delta Character", wins=0, losses=0, level=2))
    write_character(characters_dir, "echo", base_character("Echo Character", wins=3, losses=3, level=1))


def test_message_12_leaderboard_builds_leaderboard_in_ooc_room(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    setup_leaderboard_characters(characters_dir)

    monkeypatch.chdir(tmp_path)

    msg = message_12_leaderboard(
        channel="ooc-room",
        charFolder=str(characters_dir) + "/",
        unspoiledBarOOC="ooc-room",
        message="!leaderboard win",
    )

    assert len(msg) == 1
    assert "Charlie Character (charlie, Level: [color=green]5[/color])" in msg[0]
    assert msg[0].index("Charlie Character") < msg[0].index("Alpha Character")


def test_message_12_leaderboard_rejects_wrong_channel(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    setup_leaderboard_characters(characters_dir)

    monkeypatch.chdir(tmp_path)

    msg = message_12_leaderboard(
        channel="wrong-room",
        charFolder=str(characters_dir) + "/",
        unspoiledBarOOC="ooc-room",
        message="!leaderboard win",
    )

    assert msg == "This Command can only be used in [session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]"