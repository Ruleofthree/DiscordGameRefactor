from src.character_repository import build_challenge_accept_initiative_result


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