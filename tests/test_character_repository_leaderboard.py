import json

from src.character_repository import build_character_leaderboard_messages


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


def write_player_database(characters_dir):
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


def setup_leaderboard_characters(characters_dir):
    write_player_database(characters_dir)

    write_character(
        characters_dir,
        "alpha",
        base_character("Alpha Character", wins=5, losses=2, level=3),
    )
    write_character(
        characters_dir,
        "bravo",
        base_character("Bravo Character", wins=1, losses=8, level=4),
    )
    write_character(
        characters_dir,
        "charlie",
        base_character("Charlie Character", wins=10, losses=0, level=5),
    )
    write_character(
        characters_dir,
        "delta",
        base_character("Delta Character", wins=0, losses=0, level=2),
    )
    write_character(
        characters_dir,
        "echo",
        base_character("Echo Character", wins=3, losses=3, level=1),
    )


def test_build_character_leaderboard_messages_sorts_by_wins(tmp_path):
    setup_leaderboard_characters(tmp_path)

    msg = build_character_leaderboard_messages(tmp_path, "win")

    assert len(msg) == 1
    assert "Charlie Character (charlie, Level: [color=green]5[/color])" in msg[0]
    assert msg[0].index("Charlie Character") < msg[0].index("Alpha Character")
    assert msg[0].index("Alpha Character") < msg[0].index("Echo Character")


def test_build_character_leaderboard_messages_sorts_by_losses(tmp_path):
    setup_leaderboard_characters(tmp_path)

    msg = build_character_leaderboard_messages(tmp_path, "loss")

    assert len(msg) == 1
    assert msg[0].index("Bravo Character") < msg[0].index("Echo Character")
    assert msg[0].index("Echo Character") < msg[0].index("Alpha Character")


def test_build_character_leaderboard_messages_sorts_by_percent(tmp_path):
    setup_leaderboard_characters(tmp_path)

    msg = build_character_leaderboard_messages(tmp_path, "percent")

    assert len(msg) == 1
    assert msg[0].index("Charlie Character") < msg[0].index("Alpha Character")
    assert msg[0].index("Alpha Character") < msg[0].index("Echo Character")
    assert "(100.0%)" in msg[0]


def test_build_character_leaderboard_messages_defaults_to_wins_for_unknown_category(tmp_path):
    setup_leaderboard_characters(tmp_path)

    msg = build_character_leaderboard_messages(tmp_path, "nonsense")

    assert len(msg) == 1
    assert msg[0].index("Charlie Character") < msg[0].index("Alpha Character")


def test_build_character_leaderboard_messages_handles_zero_total_as_zero_percent(tmp_path):
    setup_leaderboard_characters(tmp_path)

    msg = build_character_leaderboard_messages(tmp_path, "percent")

    assert "Delta Character (delta, Level: [color=green]2[/color])" in msg[0]
    assert "0%)" in msg[0]