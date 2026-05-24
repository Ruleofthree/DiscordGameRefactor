from src.character_repository import build_character_challenge_message


def make_character(name, hidden_feats=None, total_feats=2, trait=""):
    if hidden_feats is None:
        hidden_feats = ["feat one", "feat two"]

    return {
        "name": name,
        "hfeats taken": hidden_feats,
        "total feats": total_feats,
        "trait": trait,
    }


def test_build_character_challenge_message_rejects_self_challenge():
    challenger = make_character("Alice Hero")
    opponent = make_character("Alice Hero")

    result = build_character_challenge_message(
        challenger,
        opponent,
        opponent_profile="alice",
        challenger_profile="alice",
    )

    assert result == "You can't fight yourself. No one is that special."


def test_build_character_challenge_message_rejects_challenger_with_empty_feat_slots():
    challenger = make_character("Alice Hero", hidden_feats=["feat one"], total_feats=2)
    opponent = make_character("Bob Hero")

    result = build_character_challenge_message(
        challenger,
        opponent,
        opponent_profile="bob",
        challenger_profile="alice",
    )

    assert result == "Alice Hero has empty feat slots, and cannot fight yet"


def test_build_character_challenge_message_rejects_opponent_with_empty_feat_slots():
    challenger = make_character("Alice Hero")
    opponent = make_character("Bob Hero", hidden_feats=["feat one"], total_feats=2)

    result = build_character_challenge_message(
        challenger,
        opponent,
        opponent_profile="bob",
        challenger_profile="alice",
    )

    assert result == "Bob Hero has empty feat slots, and cannot fight yet"


def test_build_character_challenge_message_builds_standard_challenge_message():
    challenger = make_character("Alice Hero")
    opponent = make_character("Bob Hero")

    result = build_character_challenge_message(
        challenger,
        opponent,
        opponent_profile="bob",
        challenger_profile="alice",
    )

    assert result == (
        "Alice Hero is challenging Bob Hero (Bob, "
        "Type [color=pink]!accept[/color])"
    )


def test_build_character_challenge_message_warns_when_either_character_is_cursed():
    challenger = make_character("Alice Hero", trait="cursed")
    opponent = make_character("Bob Hero")

    result = build_character_challenge_message(
        challenger,
        opponent,
        opponent_profile="bob",
        challenger_profile="alice",
    )

    assert result == (
        "Alice Hero is challenging Bob Hero (Bob, "
        "Type [color=pink]!accept[/color]) Please be aware that one of the opponents"
        " is [color=cyan]cursed[/color], and no xp/renown will be awarded at end of match."
    )