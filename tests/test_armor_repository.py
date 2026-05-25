import pytest

from src.armor_repository import (
    build_armor_shop_display,
    buy_character_armor,
    get_armor_dictionary,
    get_armor_effects,
    get_armor_shop_lists,
    stock_armor_shop,
)


def test_get_armor_dictionary_returns_loaded_armor_data():
    result = get_armor_dictionary()

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "cat1" in result[0]
    assert "cat2" in result[0]
    assert "cat3" in result[0]
    assert "armorlist" in result[0]


def test_get_armor_shop_lists_returns_legacy_shape():
    result = get_armor_shop_lists()

    assert isinstance(result, tuple)
    assert len(result) == 9


def test_get_armor_shop_lists_returns_cat_one_common_items():
    cat_one_common = get_armor_shop_lists()[0]

    assert cat_one_common == [
        "str1",
        "str2",
        "dex1",
        "dex2",
        "con1",
        "con2",
    ]


def test_get_armor_shop_lists_returns_cat_two_common_items():
    cat_two_common = get_armor_shop_lists()[3]

    assert cat_two_common == [
        "init1",
        "init2",
        "ac1",
        "ac2",
        "hp5",
        "hp10",
        "dr1",
        "dr2",
    ]


def test_get_armor_shop_lists_returns_cat_three_rare_items():
    cat_three_rare = get_armor_shop_lists()[8]

    assert cat_three_rare == [
        "blur5",
        "damage5",
        "hit5",
    ]


def test_get_armor_effects_returns_effects_for_valid_armor_key():
    result = get_armor_effects("armor4")

    assert result == ["dex2", "ac2"]


def test_get_armor_effects_returns_multiple_effects_for_valid_armor_key():
    result = get_armor_effects("armor8")

    assert result == ["con4", "hp15", "hit4"]


def test_get_armor_effects_raises_key_error_for_invalid_armor_key():
    with pytest.raises(KeyError):
        get_armor_effects("not-real-armor")


def test_build_armor_shop_display_formats_single_attribute_armor():
    result = build_armor_shop_display([
        ["str1"],
    ])

    assert result == "Armor1 [color=red]['str1'][/color]: [color=yellow](500 renown)[/color]"


def test_build_armor_shop_display_formats_two_attribute_armor():
    result = build_armor_shop_display([
        ["dex2", "ac2"],
    ])

    assert result == "Armor1 [color=red]['dex2', 'ac2'][/color]: [color=yellow](5000 renown)[/color]"


def test_build_armor_shop_display_formats_three_attribute_armor():
    result = build_armor_shop_display([
        ["con4", "hp15", "hit4"],
    ])

    assert result == "Armor1 [color=red]['con4', 'hp15', 'hit4'][/color]: [color=yellow](12500 renown)[/color]"


def test_build_armor_shop_display_formats_sold_armor():
    result = build_armor_shop_display([
        "sold",
    ])

    assert result == "Armor1 [color=red]sold[/color]: [color=yellow](0 renown)[/color]"


def test_build_armor_shop_display_preserves_multiple_line_display():
    result = build_armor_shop_display([
        ["str1"],
        ["dex2", "ac2"],
        ["con4", "hp15", "hit4"],
        "sold",
    ])

    assert result == (
        "Armor1 [color=red]['str1'][/color]: [color=yellow](500 renown)[/color]\n"
        "Armor2 [color=red]['dex2', 'ac2'][/color]: [color=yellow](5000 renown)[/color]\n"
        "Armor3 [color=red]['con4', 'hp15', 'hit4'][/color]: [color=yellow](12500 renown)[/color]\n"
        "Armor4 [color=red]sold[/color]: [color=yellow](0 renown)[/color]"
    )


def test_stock_armor_shop_stocks_twenty_cat_one_common_items(monkeypatch):
    armor_dictionary = get_armor_dictionary()

    randint_values = iter([
        41, 1,
    ] * 20)

    monkeypatch.setattr("random.randint", lambda start, end: next(randint_values))
    monkeypatch.setattr("random.choice", lambda choices: choices[0])

    updated_armor, message = stock_armor_shop(
        armor_dictionary,
        ["str1"],
        ["str3"],
        ["str5"],
        ["ac1"],
        ["ac3"],
        ["ac5"],
        ["hit1"],
        ["hit3"],
        ["hit5"],
    )

    expected_armor_list = {
        "armor" + str(number): ["str1"]
        for number in range(1, 21)
    }

    assert updated_armor[0]["armorlist"] == expected_armor_list
    assert message == "Armor Shop has been stocked for the week."


def test_stock_armor_shop_can_stock_three_attribute_items(monkeypatch):
    armor_dictionary = get_armor_dictionary()

    randint_values = iter([
        1, 1, 1, 1,
    ] * 20)

    monkeypatch.setattr("random.randint", lambda start, end: next(randint_values))
    monkeypatch.setattr("random.choice", lambda choices: choices[0])

    updated_armor, message = stock_armor_shop(
        armor_dictionary,
        ["str1"],
        ["str3"],
        ["str5"],
        ["ac1"],
        ["ac3"],
        ["ac5"],
        ["hit1"],
        ["hit3"],
        ["hit5"],
    )

    expected_armor_list = {
        "armor" + str(number): ["str1", "ac1", "hit1"]
        for number in range(1, 21)
    }

    assert updated_armor[0]["armorlist"] == expected_armor_list
    assert message == "Armor Shop has been stocked for the week."


def test_buy_character_armor_purchases_available_armor():
    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {"ac1": [2000, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": ["str1", "ac1"],
            },
        }
    ]

    char_sheet = {
        "name": "Test Character",
        "renown": 3000,
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, updated_armor, msg = buy_character_armor(
        char_sheet,
        armor_data,
        "armor1",
    )

    assert updated_char["renown"] == 500
    assert updated_char["armor"]["armor1"] == ["str1", "ac1", 2500]
    assert updated_armor[0]["armorlist"]["armor1"] == "sold"
    assert msg == "Test Character has purchased an armor of [color=red]str1, ac1[/color]."


def test_buy_character_armor_rejects_invalid_armor_key():
    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": ["str1"],
            },
        }
    ]

    char_sheet = {
        "name": "Test Character",
        "renown": 3000,
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, updated_armor, msg = buy_character_armor(
        char_sheet,
        armor_data,
        "not-real-armor",
    )

    assert updated_char == char_sheet
    assert updated_armor == armor_data
    assert msg == "You seemed to have not typed in your desired choice correctly."


def test_buy_character_armor_rejects_sold_armor():
    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": "sold",
            },
        }
    ]

    char_sheet = {
        "name": "Test Character",
        "renown": 3000,
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, updated_armor, msg = buy_character_armor(
        char_sheet,
        armor_data,
        "armor1",
    )

    assert updated_char == char_sheet
    assert updated_armor == armor_data
    assert msg == "This armor has already been sold."


def test_buy_character_armor_rejects_insufficient_renown():
    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {"ac1": [2000, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": ["str1", "ac1"],
            },
        }
    ]

    char_sheet = {
        "name": "Test Character",
        "renown": 100,
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, updated_armor, msg = buy_character_armor(
        char_sheet,
        armor_data,
        "armor1",
    )

    assert updated_char["renown"] == 100
    assert updated_char["armor"]["armor1"] == "n/a"
    assert updated_armor[0]["armorlist"]["armor1"] == ["str1", "ac1"]
    assert msg == "You do not have enough renown to purchase this."


def test_buy_character_armor_rejects_full_inventory():
    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {"ac1": [2000, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": ["str1", "ac1"],
            },
        }
    ]

    char_sheet = {
        "name": "Test Character",
        "renown": 3000,
        "armor": {
            "armor1": ["old1", 100],
            "armor2": ["old2", 200],
            "armor3": ["old3", 300],
        },
    }

    updated_char, updated_armor, msg = buy_character_armor(
        char_sheet,
        armor_data,
        "armor1",
    )

    assert updated_char["renown"] == 3000
    assert updated_char["armor"]["armor1"] == ["old1", 100]
    assert updated_char["armor"]["armor2"] == ["old2", 200]
    assert updated_char["armor"]["armor3"] == ["old3", 300]
    assert updated_armor[0]["armorlist"]["armor1"] == ["str1", "ac1"]
    assert msg == "You do not have enough inventory space to own more armor."


def test_buy_character_armor_uses_first_available_inventory_slot():
    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {"ac1": [2000, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": ["str1", "ac1"],
            },
        }
    ]

    char_sheet = {
        "name": "Test Character",
        "renown": 3000,
        "armor": {
            "armor1": ["old1", 100],
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, updated_armor, msg = buy_character_armor(
        char_sheet,
        armor_data,
        "armor1",
    )

    assert updated_char["renown"] == 500
    assert updated_char["armor"]["armor1"] == ["old1", 100]
    assert updated_char["armor"]["armor2"] == ["str1", "ac1", 2500]
    assert updated_char["armor"]["armor3"] == "n/a"
    assert updated_armor[0]["armorlist"]["armor1"] == "sold"
    assert msg == "Test Character has purchased an armor of [color=red]str1, ac1[/color]."


