import pytest

from src.armor_repository import (
    build_armor_shop_display,
    buy_character_armor,
    get_armor_dictionary,
    get_armor_effects,
    get_armor_shop_lists,
    sell_character_armor,
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


def make_armor_character():
    return {
        "name": "Test Character",
        "equip": "",
        "armor": {
            "armor1": "n/a",
            "old armor": ["str1", 500],
            "existing armor": ["dex1", 500],
        },
    }


def test_rename_character_armor_renames_owned_armor():
    from src.armor_repository import rename_character_armor

    character_data = make_armor_character()

    msg = rename_character_armor(
        character_data,
        armor_name="new armor",
        armor_remove="old armor",
    )

    assert msg == "Test Character renamed old armor to new armor."
    assert "old armor" not in character_data["armor"]
    assert character_data["armor"]["new armor"] == ["str1", 500]


def test_rename_character_armor_rejects_missing_inventory_key():
    from src.armor_repository import rename_character_armor

    character_data = make_armor_character()
    original_armor = character_data["armor"].copy()

    msg = rename_character_armor(
        character_data,
        armor_name="new armor",
        armor_remove="missing armor",
    )

    assert msg == (
        "missing armor is not within your inventory to rename. Please check you are typing armor name correctly,"
        " then try this command again"
    )
    assert character_data["armor"] == original_armor


def test_rename_character_armor_rejects_duplicate_new_name():
    from src.armor_repository import rename_character_armor

    character_data = make_armor_character()
    original_armor = character_data["armor"].copy()

    msg = rename_character_armor(
        character_data,
        armor_name="existing armor",
        armor_remove="old armor",
    )

    assert msg == (
        "You already have a piece of armor named existing armor. Please use a new name, and try this command "
        "again"
    )
    assert character_data["armor"] == original_armor


def test_rename_character_armor_rejects_equipped_armor():
    from src.armor_repository import rename_character_armor

    character_data = make_armor_character()
    character_data["equip"] = "old armor"
    original_armor = character_data["armor"].copy()

    msg = rename_character_armor(
        character_data,
        armor_name="new armor",
        armor_remove="old armor",
    )

    assert msg == "You need to unequip the armor first, before using this command."
    assert character_data["armor"] == original_armor


def test_rename_character_armor_rejects_empty_armor_slot():
    from src.armor_repository import rename_character_armor

    character_data = make_armor_character()
    original_armor = character_data["armor"].copy()

    msg = rename_character_armor(
        character_data,
        armor_name="new armor",
        armor_remove="armor1",
    )

    assert msg == "There is no armor in that slot to rename. Please double check inventory, then use this command again."
    assert character_data["armor"] == original_armor


def make_equipped_armor_character():
    return {
        "name": "Test Character",
        "equip": "old armor",
        "armor": {
            "old armor": ["str1", "hp10", 500],
        },
        "armorhit": 1,
        "armordamage": 2,
        "armorac": 3,
        "armorhp": 10,
        "armordr": 4,
        "armorinitiative": 5,
        "armorstrength": 6,
        "armordexterity": 7,
        "armorconstitution": 8,
        "armorblur": 9,
    }


def test_unequip_character_armor_clears_equipped_armor_and_armor_bonuses():
    from src.armor_repository import unequip_character_armor

    character_data = make_equipped_armor_character()

    msg = unequip_character_armor(character_data, "old armor")

    assert msg == "Test Character has unequipped old armor"
    assert character_data["equip"] == ""
    assert character_data["armorhit"] == 0
    assert character_data["armordamage"] == 0
    assert character_data["armorac"] == 0
    assert character_data["armorhp"] == 0
    assert character_data["armordr"] == 0
    assert character_data["armorinitiative"] == 0
    assert character_data["armorstrength"] == 0
    assert character_data["armordexterity"] == 0
    assert character_data["armorconstitution"] == 0
    assert character_data["armorblur"] == 0


def test_unequip_character_armor_does_not_validate_armor_name():
    from src.armor_repository import unequip_character_armor

    character_data = make_equipped_armor_character()

    msg = unequip_character_armor(character_data, "missing armor")

    assert msg == "Test Character has unequipped missing armor"
    assert character_data["equip"] == ""
    assert character_data["armorhit"] == 0
    assert character_data["armordamage"] == 0
    assert character_data["armorac"] == 0
    assert character_data["armorhp"] == 0
    assert character_data["armordr"] == 0
    assert character_data["armorinitiative"] == 0
    assert character_data["armorstrength"] == 0
    assert character_data["armordexterity"] == 0
    assert character_data["armorconstitution"] == 0
    assert character_data["armorblur"] == 0


def make_equip_armor_character():
    return {
        "name": "Test Character",
        "equip": "old armor",
        "armor": {
            "old armor": ["str1", 500],
            "new armor": ["str2", "hp10", "damage3", 500],
            "defense armor": ["dex2", "ac2", "hit4", 500],
            "dr armor": ["con1", "dr2", 500],
            "initiative armor": ["dex1", "init2", "blur1", 500],
        },
        "armorhit": 9,
        "armordamage": 9,
        "armorac": 9,
        "armorhp": 9,
        "armordr": 9,
        "armorinitiative": 9,
        "armorstrength": 9,
        "armordexterity": 9,
        "armorconstitution": 9,
        "armorblur": 9,
        "initiative": 0,
        "traitdr": 0,
        "regeneration": 0,
    }


def make_test_armor_dictionary():
    return [
        {
            "cat1": {
                "common": {
                    "str1": [500, 1],
                    "str2": [1000, 2],
                    "dex1": [500, 1],
                    "dex2": [1000, 2],
                    "con1": [500, 1],
                },
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {
                    "hp10": [1000, 10],
                    "ac2": [4000, 2],
                    "dr2": [5000, 2],
                    "init2": [750, 2],
                },
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {
                    "blur1": [5000, 1],
                },
                "uncommon": {
                    "damage3": [4500, 3],
                    "hit4": [6000, 4],
                },
                "rare": {},
            },
        }
    ]


def test_equip_character_armor_equips_owned_armor_and_applies_bonuses():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "new armor", armor_dictionary)

    assert msg == "Test Character has equipped new armor"
    assert character_data["equip"] == "new armor"
    assert character_data["armorstrength"] == 2
    assert character_data["armorhp"] == 10
    assert character_data["armordamage"] == 3

    assert character_data["armorhit"] == 0
    assert character_data["armorac"] == 0
    assert character_data["armordr"] == 0
    assert character_data["armorinitiative"] == 0
    assert character_data["armordexterity"] == 0
    assert character_data["armorconstitution"] == 0
    assert character_data["armorblur"] == 0


def test_equip_character_armor_applies_dex_ac_and_hit_bonuses():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "defense armor", armor_dictionary)

    assert msg == "Test Character has equipped defense armor"
    assert character_data["equip"] == "defense armor"
    assert character_data["armordexterity"] == 2
    assert character_data["armorac"] == 2
    assert character_data["armorhit"] == 4


def test_equip_character_armor_applies_dr_when_no_traitdr_or_regeneration():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "dr armor", armor_dictionary)

    assert msg == "Test Character has equipped dr armor"
    assert character_data["equip"] == "dr armor"
    assert character_data["armorconstitution"] == 1
    assert character_data["armordr"] == 2


def test_equip_character_armor_does_not_apply_dr_when_traitdr_exists():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    character_data["traitdr"] = 1
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "dr armor", armor_dictionary)

    assert msg == "Test Character has equipped dr armor"
    assert character_data["equip"] == "dr armor"
    assert character_data["armorconstitution"] == 1
    assert character_data["armordr"] == 0


def test_equip_character_armor_does_not_apply_dr_when_regeneration_exists():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    character_data["regeneration"] = 1
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "dr armor", armor_dictionary)

    assert msg == "Test Character has equipped dr armor"
    assert character_data["equip"] == "dr armor"
    assert character_data["armorconstitution"] == 1
    assert character_data["armordr"] == 0


def test_equip_character_armor_applies_initiative_to_both_fields_and_blur():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "initiative armor", armor_dictionary)

    assert msg == "Test Character has equipped initiative armor"
    assert character_data["equip"] == "initiative armor"
    assert character_data["armordexterity"] == 1
    assert character_data["armorinitiative"] == 2
    assert character_data["initiative"] == 2
    assert character_data["armorblur"] == 1


def test_equip_character_armor_invalid_name_still_clears_armor_bonuses():
    from src.armor_repository import equip_character_armor

    character_data = make_equip_armor_character()
    armor_dictionary = make_test_armor_dictionary()

    msg = equip_character_armor(character_data, "missing armor", armor_dictionary)

    assert msg == (
        "missing armor doesn't exist in your inventory. Make sure you are typing the armor name correctly when using"
        " this command"
    )

    # Legacy behavior: invalid equip still clears previous armor bonuses.
    assert character_data["equip"] == "old armor"
    assert character_data["armorhit"] == 0
    assert character_data["armordamage"] == 0
    assert character_data["armorac"] == 0
    assert character_data["armorhp"] == 0
    assert character_data["armordr"] == 0
    assert character_data["armorinitiative"] == 0
    assert character_data["armorstrength"] == 0
    assert character_data["armordexterity"] == 0
    assert character_data["armorconstitution"] == 0
    assert character_data["armorblur"] == 0


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


def test_sell_character_armor_sells_owned_armor_for_half_stored_price():
    char_sheet = {
        "name": "Test Character",
        "renown": 100,
        "equip": "",
        "armor": {
            "armor1": ["str1", "ac1", 2500],
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, msg = sell_character_armor(
        char_sheet,
        "armor1",
        "tester",
    )

    assert updated_char["renown"] == 1350
    assert updated_char["armor"]["armor1"] == "n/a"
    assert msg == "tester sold some armor for [color=yellow] 1250 renown[/color]"


def test_sell_character_armor_rejects_equipped_armor():
    char_sheet = {
        "name": "Test Character",
        "renown": 100,
        "equip": "armor1",
        "armor": {
            "armor1": ["str1", "ac1", 2500],
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, msg = sell_character_armor(
        char_sheet,
        "armor1",
        "tester",
    )

    assert updated_char == char_sheet
    assert msg == "You can't sell armor that is currently equipped."


def test_sell_character_armor_rejects_missing_armor_key():
    char_sheet = {
        "name": "Test Character",
        "renown": 100,
        "equip": "",
        "armor": {
            "armor1": ["str1", "ac1", 2500],
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    updated_char, msg = sell_character_armor(
        char_sheet,
        "not-real-armor",
        "tester",
    )

    assert updated_char == char_sheet
    assert msg == "You do not have that armor to sell."


