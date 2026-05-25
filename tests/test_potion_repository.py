from src.potion_repository import (
    POTION_RARITY_ORDER,
    find_potion,
    get_potion_description,
    get_potion_dictionary,
    get_potion_effect_info,
    get_potion_effect_value,
    get_potion_price,
    get_potion_sell_value,
    get_potion_shop_lists,
    sell_character_potion,
)

def test_find_potion_returns_rarity_and_data_for_common_potion():
    result = find_potion("hp5")

    assert result is not None

    rarity, potion_info = result

    assert rarity == "common"
    assert potion_info[0] == 150
    assert potion_info[2] == 5


def test_find_potion_returns_rarity_and_data_for_vrare_potion():
    result = find_potion("damage5")

    assert result is not None

    rarity, potion_info = result

    assert rarity == "vrare"
    assert potion_info[0] == 2000
    assert potion_info[2] == 5


def test_find_potion_returns_none_for_unknown_potion():
    result = find_potion("fake potion")

    assert result is None


def test_get_potion_price_returns_expected_price():
    assert get_potion_price("hp5") == 150


def test_get_potion_description_returns_expected_description():
    assert get_potion_description("hp5") == "increasing hp by 5 for duration of fight"


def test_get_potion_effect_value_returns_expected_value():
    assert get_potion_effect_value("hp5") == 5


def test_get_potion_helpers_return_none_for_unknown_potion():
    assert get_potion_price("fake potion") is None
    assert get_potion_description("fake potion") is None
    assert get_potion_effect_value("fake potion") is None

def test_get_potion_sell_value_returns_half_price():
        assert get_potion_sell_value("hp5") == 75


def test_get_potion_sell_value_returns_none_for_unknown_potion():
        assert get_potion_sell_value("fake potion") is None


def test_get_potion_effect_info_returns_effect_and_description():
    result = get_potion_effect_info("hp5")

    assert result == (5, "increasing hp by 5 for duration of fight")


def test_get_potion_effect_info_returns_none_for_unknown_potion():
    assert get_potion_effect_info("fake potion") is None


def test_sell_character_potion_sells_owned_potion_and_adds_half_value():
    character_data = {
        "name": "Test Hero",
        "renown": 100,
        "potions": ["hp5"],
    }

    updated_character, message = sell_character_potion(character_data, "hp5")

    assert message == "Test Hero has sold a [color=red]hp5[/color] for [color=yellow]75 renown[/color]."
    assert updated_character["renown"] == 175
    assert updated_character["potions"] == []


def test_sell_character_potion_rejects_missing_potion_without_changing_character():
    character_data = {
        "name": "Test Hero",
        "renown": 100,
        "potions": ["hp5"],
    }

    updated_character, message = sell_character_potion(character_data, "damage1")

    assert message == "You do not have that potion to sell."
    assert updated_character["renown"] == 100
    assert updated_character["potions"] == ["hp5"]


def test_sell_character_potion_rejects_unknown_potion_data_without_changing_character():
    character_data = {
        "name": "Test Hero",
        "renown": 100,
        "potions": ["fake potion"],
    }

    updated_character, message = sell_character_potion(character_data, "fake potion")

    assert message == "That potion does not exist in the potion data."
    assert updated_character["renown"] == 100
    assert updated_character["potions"] == ["fake potion"]