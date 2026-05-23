import pytest
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onMSGUtils import message_10_challenge


def make_character_file(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def make_ready_character(name, total_feats=2, hidden_feats=None, trait="brawler"):
    if hidden_feats is None:
        hidden_feats = ["feat one", "feat two"]

    return {
        "name": name,
        "level": 1,
        "trait": trait,
        "total feats": total_feats,
        "hfeats taken": hidden_feats,
    }


def test_message_10_challenge_wrong_channel_has_legacy_unbound_local_error(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    with pytest.raises(UnboundLocalError):
        message_10_challenge(
            channel="wrong-room",
            charFolder=str(characters_dir) + "\\",
            message="!challenge opponent profile",
            unspoiledArena="arena-room",
            character="challenger profile",
            game=0,
        )


def test_message_10_challenge_active_game_has_legacy_unbound_local_error(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    with pytest.raises(UnboundLocalError):
        message_10_challenge(
            channel="arena-room",
            charFolder=str(characters_dir) + "\\",
            message="!challenge opponent profile",
            unspoiledArena="arena-room",
            character="challenger profile",
            game=1,
        )


def test_message_10_challenge_pending_game_has_legacy_unbound_local_error(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    with pytest.raises(UnboundLocalError):
        message_10_challenge(
            channel="arena-room",
            charFolder=str(characters_dir) + "\\",
            message="!challenge opponent profile",
            unspoiledArena="arena-room",
            character="challenger profile",
            game=0.5,
        )


def test_message_10_challenge_rejects_challenger_without_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    result = message_10_challenge(
        channel="arena-room",
        charFolder=str(characters_dir) + "\\",
        message="!challenge opponent profile",
        unspoiledArena="arena-room",
        character="challenger profile",
        game=0,
    )

    assert result == ("You don't even have a character made to fight.", False)


def test_message_10_challenge_starts_pending_challenge_for_valid_characters(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "challenger profile",
        make_ready_character("Challenger Hero"),
    )

    make_character_file(
        characters_dir,
        "opponent profile",
        make_ready_character("Opponent Hero"),
    )

    result = message_10_challenge(
        channel="arena-room",
        charFolder=str(characters_dir) + "\\",
        message="!challenge opponent profile",
        unspoiledArena="arena-room",
        character="challenger profile",
        game=0,
    )

    msg, opponent, p_one_info, new_game, b_timer, player_one, update = result

    assert "Challenger Hero is challenging Opponent Hero" in msg
    assert "Type [color=pink]!accept[/color]" in msg
    assert opponent == "opponent profile"
    assert p_one_info["name"] == "Challenger Hero"
    assert new_game == 0.5
    assert b_timer is True
    assert player_one == "challenger profile"
    assert update is True


def test_message_10_challenge_rejects_self_challenge(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "challenger profile",
        make_ready_character("Challenger Hero"),
    )

    result = message_10_challenge(
        channel="arena-room",
        charFolder=str(characters_dir) + "\\",
        message="!challenge challenger profile",
        unspoiledArena="arena-room",
        character="challenger profile",
        game=0,
    )

    msg, opponent, p_one_info, new_game, b_timer, player_one, update = result

    assert msg == "You can't fight yourself. No one is that special."
    assert opponent == "challenger profile"
    assert p_one_info["name"] == "Challenger Hero"
    assert new_game == 0
    assert b_timer is False
    assert player_one == "challenger profile"
    assert update is False


def test_message_10_challenge_rejects_challenger_with_empty_feat_slots(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "challenger profile",
        make_ready_character(
            "Challenger Hero",
            total_feats=2,
            hidden_feats=["feat one"],
        ),
    )

    make_character_file(
        characters_dir,
        "opponent profile",
        make_ready_character("Opponent Hero"),
    )

    result = message_10_challenge(
        channel="arena-room",
        charFolder=str(characters_dir) + "\\",
        message="!challenge opponent profile",
        unspoiledArena="arena-room",
        character="challenger profile",
        game=0,
    )

    msg, opponent, p_one_info, new_game, b_timer, player_one, update = result

    assert msg == "Challenger Hero has empty feat slots, and cannot fight yet"
    assert opponent == "opponent profile"
    assert p_one_info["name"] == "Challenger Hero"
    assert new_game == 0
    assert b_timer is False
    assert player_one == "challenger profile"
    assert update is False


def test_message_10_challenge_rejects_opponent_with_empty_feat_slots(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "challenger profile",
        make_ready_character("Challenger Hero"),
    )

    make_character_file(
        characters_dir,
        "opponent profile",
        make_ready_character(
            "Opponent Hero",
            total_feats=2,
            hidden_feats=["feat one"],
        ),
    )

    result = message_10_challenge(
        channel="arena-room",
        charFolder=str(characters_dir) + "\\",
        message="!challenge opponent profile",
        unspoiledArena="arena-room",
        character="challenger profile",
        game=0,
    )

    msg, opponent, p_one_info, new_game, b_timer, player_one, update = result

    assert msg == "Opponent Hero has empty feat slots, and cannot fight yet"
    assert opponent == "opponent profile"
    assert p_one_info["name"] == "Challenger Hero"
    assert new_game == 0
    assert b_timer is False
    assert player_one == "challenger profile"
    assert update is False


def test_message_10_challenge_warns_when_one_character_is_cursed(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "challenger profile",
        make_ready_character("Challenger Hero", trait="cursed"),
    )

    make_character_file(
        characters_dir,
        "opponent profile",
        make_ready_character("Opponent Hero"),
    )

    result = message_10_challenge(
        channel="arena-room",
        charFolder=str(characters_dir) + "\\",
        message="!challenge opponent profile",
        unspoiledArena="arena-room",
        character="challenger profile",
        game=0,
    )

    msg, opponent, p_one_info, new_game, b_timer, player_one, update = result

    assert "Please be aware that one of the opponents is [color=cyan]cursed[/color]" in msg
    assert opponent == "opponent profile"
    assert p_one_info["name"] == "Challenger Hero"
    assert new_game == 0.5
    assert b_timer is True
    assert player_one == "challenger profile"
    assert update is True