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
    stock_potion_shop,
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


def test_stock_potion_shop_replaces_shoplist_with_twenty_common_potions(monkeypatch):
    potion_data = [
        {
            "shoplist": ["old potion"],
            "common": {
                "common0": [10, "common zero", 0],
                "common1": [20, "common one", 1],
            },
            "uncommon": {
                "uncommon0": [30, "uncommon zero", 0],
                "uncommon1": [40, "uncommon one", 1],
            },
            "rare": {
                "rare0": [50, "rare zero", 0],
                "rare1": [60, "rare one", 1],
            },
            "vrare": {
                "vrare0": [70, "vrare zero", 0],
                "vrare1": [80, "vrare one", 1],
            },
            "relic": {
                "relic0": [90, "relic zero", 0],
                "relic1": [100, "relic one", 1],
            },
        }
    ]

    monkeypatch.setattr("random.randint", lambda start, end: 1)

    updated_data, msg, shop_string = stock_potion_shop(
        potion_data,
        ["common0", "common1"],
        ["uncommon0", "uncommon1"],
        ["rare0", "rare1"],
        ["vrare0", "vrare1"],
        ["relic0", "relic1"],
    )

    expected_shop = ["common1"] * 20

    assert updated_data[0]["shoplist"] == expected_shop
    assert shop_string == ", ".join(expected_shop)
    assert msg == "Shop stocked for the week as follows: \n" + shop_string


def test_stock_potion_shop_can_stock_each_rarity_bucket(monkeypatch):
    potion_data = [
        {
            "shoplist": [],
            "common": {
                "common0": [10, "common zero", 0],
                "common1": [20, "common one", 1],
            },
            "uncommon": {
                "uncommon0": [30, "uncommon zero", 0],
                "uncommon1": [40, "uncommon one", 1],
            },
            "rare": {
                "rare0": [50, "rare zero", 0],
                "rare1": [60, "rare one", 1],
            },
            "vrare": {
                "vrare0": [70, "vrare zero", 0],
                "vrare1": [80, "vrare one", 1],
            },
            "relic": {
                "relic0": [90, "relic zero", 0],
                "relic1": [100, "relic one", 1],
            },
        }
    ]

    rolls = iter([
        1, 1,
        51, 1,
        77, 1,
        90, 1,
        98, 1,
    ] * 4)

    monkeypatch.setattr("random.randint", lambda start, end: next(rolls))

    updated_data, msg, shop_string = stock_potion_shop(
        potion_data,
        ["common0", "common1"],
        ["uncommon0", "uncommon1"],
        ["rare0", "rare1"],
        ["vrare0", "vrare1"],
        ["relic0", "relic1"],
    )

    expected_shop = [
        "common1",
        "uncommon1",
        "rare1",
        "vrare1",
        "relic1",
    ] * 4

    assert updated_data[0]["shoplist"] == expected_shop
    assert shop_string == ", ".join(expected_shop)
    assert msg == "Shop stocked for the week as follows: \n" + shop_string