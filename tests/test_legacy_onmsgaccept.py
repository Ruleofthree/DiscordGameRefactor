import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onMSGAccept import message_accept


UNSPOILED_ARENA = "ADH-abfb9b6ebd20f1e7a693"


def write_character(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def test_message_accept_accepts_active_challenge_and_starts_fight(tmp_path, monkeypatch):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    challenger_info = {
        "name": "Alice",
        "initiative": 3,
        "thp": 30,
        "level": 1,
    }

    defender_info = {
        "name": "Bob",
        "initiative": 1,
        "thp": 28,
        "level": 1,
    }

    write_character(characters_dir, "bob", defender_info)

    monkeypatch.chdir(tmp_path)

    rolls = iter([10, 5])
    monkeypatch.setattr(
        "onMSGAccept.random.randint",
        lambda minimum, maximum: next(rolls),
    )

    (
        msg,
        p_two_info,
        new_game,
        player_two,
        b_timer,
        b_game_timer,
        new_opponent,
        token,
        update,
    ) = message_accept(
        channel=UNSPOILED_ARENA,
        charFolder=str(characters_dir) + "/",
        unspoiledArena=UNSPOILED_ARENA,
        character="Bob",
        game=0.5,
        opponent="bob",
        pOneInfo=challenger_info,
    )

    assert msg == [
        "\nRolling Initiative to see who goes first. In result of tie, person with "
        "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
        "it, coin flip. Alice wins on a One.",
        "Alice rolled: 10 + 3 and got [color=red]13[/color]\n"
        "Bob rolled: 5 + 1 and got [color=red]6[/color]",
        "Alice Goes first",
        "Type [color=pink]!usefeat <feat>[/color] to use a feat.",
    ]

    assert p_two_info == defender_info
    assert new_game == 1
    assert player_two == "bob"
    assert b_timer is True
    assert b_game_timer is True
    assert new_opponent is None
    assert token == 1
    assert update is True