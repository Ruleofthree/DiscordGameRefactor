from src.character_repository import add_ability_point


def make_character():
    return {
        "strength": 5,
        "dexterity": 4,
        "constitution": 6,
        "apboost": True,
    }


def test_add_ability_point_strength_full_name():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "strength")

    assert updated["strength"] == 6
    assert updated["dexterity"] == 4
    assert updated["constitution"] == 6
    assert updated["apboost"] is False
    assert msg == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]


def test_add_ability_point_strength_short_name():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "str")

    assert updated["strength"] == 6
    assert updated["apboost"] is False
    assert msg == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]


def test_add_ability_point_dexterity_full_name():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "dexterity")

    assert updated["dexterity"] == 5
    assert updated["strength"] == 5
    assert updated["constitution"] == 6
    assert updated["apboost"] is False
    assert msg == [
        "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]


def test_add_ability_point_dexterity_short_name():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "dex")

    assert updated["dexterity"] == 5
    assert updated["apboost"] is False
    assert msg == [
        "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]


def test_add_ability_point_constitution_full_name():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "constitution")

    assert updated["constitution"] == 7
    assert updated["strength"] == 5
    assert updated["dexterity"] == 4
    assert updated["apboost"] is False
    assert msg == [
        "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]


def test_add_ability_point_constitution_short_name():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "con")

    assert updated["constitution"] == 7
    assert updated["apboost"] is False
    assert msg == [
        "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] "
        "to ensure changes."
    ]


def test_add_ability_point_invalid_ability_does_not_change_character():
    char_data = make_character()

    updated, msg = add_ability_point(char_data, "wisdom")

    assert updated == {
        "strength": 5,
        "dexterity": 4,
        "constitution": 6,
        "apboost": True,
    }
    assert msg == [
        "You need to specify the ability you want to point the point to. "
        "Type '!add str' or '!add strength' for strength, and so on."
    ]


def test_add_ability_point_without_apboost_does_not_change_stats():
    char_data = make_character()
    char_data["apboost"] = False

    updated, msg = add_ability_point(char_data, "strength")

    assert updated["strength"] == 5
    assert updated["dexterity"] == 4
    assert updated["constitution"] == 6
    assert updated["apboost"] is False
    assert msg == ["You do not have any more ability points to spend."]