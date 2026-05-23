from src.potion_repository import (
    POTION_RARITY_ORDER,
    find_potion,
    get_potion_description,
    get_potion_dictionary,
    get_potion_effect_value,
    get_potion_price,
    get_potion_shop_lists,
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