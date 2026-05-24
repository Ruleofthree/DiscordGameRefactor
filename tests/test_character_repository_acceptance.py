import json
from src.character_repository import (build_challenge_accept_initiative_result,
                                      build_challenge_acceptance_result)


def write_character(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def test_build_challenge_accept_initiative_result_player_one_wins_by_total_roll():
    player_one = {"name": "Alice", "initiative": 3}
    player_two = {"name": "Bob", "initiative": 1}

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=10,
        player_two_roll=5,
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
    assert token == 1


def test_build_challenge_accept_initiative_result_player_two_wins_by_total_roll():
    player_one = {"name": "Alice", "initiative": 1}
    player_two = {"name": "Bob", "initiative": 4}

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=5,
        player_two_roll=10,
    )

    assert msg == [
        "\nRolling Initiative to see who goes first. In result of tie, person with "
        "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
        "it, coin flip. Alice wins on a One.",
        "Alice rolled: 5 + 1 and got [color=red]6[/color]\n"
        "Bob rolled: 10 + 4 and got [color=red]14[/color]",
        "Bob Goes first",
        "Type [color=pink]!usefeat <feat>[/color] to use a feat.",
    ]
    assert token == 2


def test_build_challenge_accept_initiative_result_player_one_wins_tied_total_by_modifier():
    player_one = {"name": "Alice", "initiative": 5}
    player_two = {"name": "Bob", "initiative": 2}

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=7,
        player_two_roll=10,
    )

    assert msg == [
        "\nRolling Initiative to see who goes first. In result of tie, person with "
        "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
        "it, coin flip. Alice wins on a One.",
        "Alice rolled: 7 + 5 and got [color=red]12[/color]\n"
        "Bob rolled: 10 + 2 and got [color=red]12[/color]",
        "Alice's dexterity: [color=red]5[/color]\nBob's dexterity: [color=red]2[/color]",
        "Alice Goes first. Type [color=pink]!usefeat <feat>[/color] to use a feat.",
    ]
    assert token == 1


def test_build_challenge_accept_initiative_result_player_two_wins_tied_total_by_modifier():
    player_one = {"name": "Alice", "initiative": 2}
    player_two = {"name": "Bob", "initiative": 5}

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=10,
        player_two_roll=7,
    )

    assert msg == [
        "\nRolling Initiative to see who goes first. In result of tie, person with "
        "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
        "it, coin flip. Alice wins on a One.",
        "Alice rolled: 10 + 2 and got [color=red]12[/color]\n"
        "Bob rolled: 7 + 5 and got [color=red]12[/color]",
        "Alice's dexterity: [color=red]2[/color]\nBob's dexterity: [color=red]5[/color]",
        "Bob Goes first. Type [color=pink]!usefeat <feat>[/color] to use a feat.",
    ]
    assert token == 2


def test_build_challenge_accept_initiative_result_player_one_wins_tied_total_and_modifier_by_coin_flip():
    player_one = {"name": "Alice", "initiative": 3}
    player_two = {"name": "Bob", "initiative": 3}

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=9,
        player_two_roll=9,
        coin_flip=1,
    )

    assert msg == [
        "\nRolling Initiative to see who goes first. In result of tie, person with "
        "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
        "it, coin flip. Alice wins on a One.",
        "Alice rolled: 9 + 3 and got [color=red]12[/color]\n"
        "Bob rolled: 9 + 3 and got [color=red]12[/color]",
        "Alice's dexterity: [color=red]3[/color]\nBob's dexterity: [color=red]3[/color]",
        "Alice Goes first. Type [color=pink]!usefeat <feat>[/color] to use a feat.",
    ]
    assert token == 1


def test_build_challenge_accept_initiative_result_player_two_wins_tied_total_and_modifier_by_coin_flip():
    player_one = {"name": "Alice", "initiative": 3}
    player_two = {"name": "Bob", "initiative": 3}

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=9,
        player_two_roll=9,
        coin_flip=2,
    )

    assert msg == [
        "\nRolling Initiative to see who goes first. In result of tie, person with "
        "highest dexterity modifier goes first. Should [b]that[/b] tie as well, then fuck "
        "it, coin flip. Alice wins on a One.",
        "Alice rolled: 9 + 3 and got [color=red]12[/color]\n"
        "Bob rolled: 9 + 3 and got [color=red]12[/color]",
        "Alice's dexterity: [color=red]3[/color]\nBob's dexterity: [color=red]3[/color]",
        "Bob Goes first. Type [color=pink]!usefeat <feat>[/color] to use a feat.",
    ]
    assert token == 2


def test_build_challenge_acceptance_result_accepts_pending_challenge(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    player_one = {
        "name": "Alice",
        "initiative": 3,
        "thp": 30,
        "level": 1,
    }

    player_two = {
        "name": "Bob",
        "initiative": 1,
        "thp": 28,
        "level": 1,
    }

    write_character(characters_dir, "bob", player_two)

    (
        msg,
        p_two_info,
        new_game,
        player_two_profile,
        b_timer,
        b_game_timer,
        new_oppenent,
        token,
        update,
    ) = build_challenge_acceptance_result(
        character="Bob",
        opponent="bob",
        player_one_info=player_one,
        player_one_roll=10,
        player_two_roll=5,
        coin_flip=None,
        characters_dir=characters_dir,
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
    assert p_two_info == player_two
    assert new_game == 1
    assert player_two_profile == "bob"
    assert b_timer is True
    assert b_game_timer is True
    assert new_oppenent is None
    assert token == 1
    assert update is True


def test_build_challenge_acceptance_result_rejects_wrong_accepting_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    player_one = {
        "name": "Alice",
        "initiative": 3,
        "thp": 30,
        "level": 1,
    }

    (
        msg,
        p_two_info,
        new_game,
        player_two_profile,
        b_timer,
        b_game_timer,
        new_oppenent,
        token,
        update,
    ) = build_challenge_acceptance_result(
        character="Charlie",
        opponent="bob",
        player_one_info=player_one,
        player_one_roll=10,
        player_two_roll=5,
        coin_flip=None,
        characters_dir=characters_dir,
    )

    assert msg == [
        "I may be a bot, but I'm pretty sure you aren't bob. A for effort, though."
    ]
    assert p_two_info is None
    assert new_game is None
    assert player_two_profile == "charlie"
    assert b_timer is False
    assert b_game_timer is False
    assert new_oppenent is None
    assert token is None
    assert update is False


def test_build_challenge_acceptance_result_handles_missing_pending_opponent(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    player_one = {
        "name": "Alice",
        "initiative": 3,
        "thp": 30,
        "level": 1,
    }

    (
        msg,
        p_two_info,
        new_game,
        player_two_profile,
        b_timer,
        b_game_timer,
        new_oppenent,
        token,
        update,
    ) = build_challenge_acceptance_result(
        character="Bob",
        opponent=None,
        player_one_info=player_one,
        player_one_roll=10,
        player_two_roll=5,
        coin_flip=None,
        characters_dir=characters_dir,
    )

    assert msg == ["Wait for the pervious challenge to expire."]
    assert p_two_info is None
    assert new_game is None
    assert player_two_profile == "bob"
    assert b_timer is False
    assert b_game_timer is False
    assert new_oppenent is None
    assert token is None
    
    assert update is False