from src.character_repository import (
    add_ability_point,
    build_challenge_accept_initiative_result,
    build_challenge_acceptance_result,
    calculate_character_view_totals,
    save_character,
)


def make_combat_ready_character(**overrides):
    character = {
        "name": "Test Hero",
        "build": "strength",
        "trait": "",
        "level": 1,
        "hp": 20,
        "total feats": 0,
        "base damage": "1d10",
        "hit": 2,
        "damage": 3,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 100,
        "strength": 4,
        "dexterity": 4,
        "constitution": 4,
        "remaining feats": 0,
        "ap": 15,
        "apboost": True,
        "regeneration": 3,
        "feats taken": [],
        "armor": {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a"},
        "equip": "",
        "hfeats taken": [],
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "forfeits": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "thp": 17,
        "tac": 12,
        "thit": 4,
        "tdamage": 6,
        "tdr": 2,
        "dexfighter": 0,
        "renown": 0,
        "initiative": 1,
        "potions": [],
        "potioneffect": "",
        "potionhit": 0,
        "potiondamage": 0,
        "potionac": 0,
        "potionhp": 0,
        "potionblur": 0,
        "potionstr": 0,
        "potiondex": 0,
        "potioncon": 0,
        "potionregen": 0,
        "pstrength": 0,
        "pdexterity": 0,
        "pconstitution": 0,
        "armorhit": 0,
        "armordamage": 0,
        "armorac": 0,
        "armorhp": 0,
        "armordr": 0,
        "armorstrength": 0,
        "armordexterity": 0,
        "armorconstitution": 0,
        "armorblur": 0,
        "armorinitiative": 0,
        "blur": 0,
        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traitdr": 0,
        "traithp": 0,
        "traitregen": 0,
        "cursed": 0,
        "status": "",
        "statuscounter": 0,
        "fight": 0,
    }
    character.update(overrides)
    return character


def test_challenge_accept_initiative_uses_saved_initiative_not_source_dexterity():
    player_one = make_combat_ready_character(
        name="Alice Hero",
        dexterity=20,
        initiative=0,
    )
    player_two = make_combat_ready_character(
        name="Bob Hero",
        dexterity=2,
        initiative=8,
    )

    msg, token = build_challenge_accept_initiative_result(
        player_one,
        player_two,
        player_one_roll=10,
        player_two_roll=3,
        coin_flip=1,
    )

    assert token == 2
    assert "Alice Hero rolled: 10 + 0 and got [color=red]10[/color]" in msg[1]
    assert "Bob Hero rolled: 3 + 8 and got [color=red]11[/color]" in msg[1]
    assert msg[2] == "Bob Hero Goes first"


def test_challenge_acceptance_returns_loaded_player_two_with_stale_saved_thp(tmp_path):
    player_one = make_combat_ready_character(
        name="Alice Hero",
        initiative=0,
        thp=19,
    )
    player_two = make_combat_ready_character(
        name="Bob Hero",
        hp=80,
        constitution=10,
        thp=17,
        initiative=5,
    )
    save_character("bob", player_two, tmp_path)

    (
        msg,
        loaded_player_two,
        new_game,
        player_two_profile,
        b_timer,
        b_game_timer,
        new_opponent,
        token,
        update,
    ) = build_challenge_acceptance_result(
        character="bob",
        opponent="bob",
        player_one_info=player_one,
        player_one_roll=10,
        player_two_roll=6,
        coin_flip=1,
        characters_dir=tmp_path,
    )

    recalculated_totals = calculate_character_view_totals(loaded_player_two)

    assert loaded_player_two["thp"] == 17
    assert recalculated_totals["thp"] != loaded_player_two["thp"]
    assert new_game == 1
    assert player_two_profile == "bob"
    assert b_timer is True
    assert b_game_timer is True
    assert new_opponent is None
    assert token == 2
    assert update is True
    assert "Bob Hero rolled: 6 + 5 and got [color=red]11[/color]" in msg[1]


def test_add_ability_point_updates_source_stat_but_preserves_saved_combat_totals():
    character = make_combat_ready_character(
        strength=5,
        thp=101,
        tac=102,
        tdr=103,
        thit=104,
        tdamage=105,
        initiative=106,
        regeneration=107,
    )

    updated, msg = add_ability_point(character, "strength")

    assert updated["strength"] == 6
    assert updated["apboost"] is False
    assert updated["thp"] == 101
    assert updated["tac"] == 102
    assert updated["tdr"] == 103
    assert updated["thit"] == 104
    assert updated["tdamage"] == 105
    assert updated["initiative"] == 106
    assert updated["regeneration"] == 107
    assert msg == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]