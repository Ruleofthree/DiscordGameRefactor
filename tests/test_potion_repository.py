from src.potion_repository import (
    POTION_RARITY_ORDER,
    buy_character_potion,
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
    use_character_potion,
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


def make_purchase_potion_data():
    return [
        {
            "shoplist": ["hp5", "damage1"],
            "common": {
                "hp5": [150, "increasing hp by 5 for duration of fight", 5],
            },
            "uncommon": {
                "damage1": [300, "increasing damage by 1 for duration of fight", 1],
            },
            "rare": {},
            "vrare": {},
            "relic": {},
        }
    ]


def test_buy_character_potion_buys_available_potion_and_updates_character_and_shop():
    potion_data = make_purchase_potion_data()
    character_data = {
        "name": "Test Hero",
        "renown": 500,
        "potions": [],
    }

    updated_character, updated_potion_data, message = buy_character_potion(
        character_data,
        potion_data,
        "hp5",
    )

    assert message == "Test Hero has puchased a potion of hp5."
    assert updated_character["renown"] == 350
    assert updated_character["potions"] == ["hp5"]
    assert updated_potion_data[0]["shoplist"] == ["damage1"]


def test_buy_character_potion_rejects_potion_not_in_shop_without_changes():
    potion_data = make_purchase_potion_data()
    character_data = {
        "name": "Test Hero",
        "renown": 500,
        "potions": [],
    }

    updated_character, updated_potion_data, message = buy_character_potion(
        character_data,
        potion_data,
        "notforsale",
    )

    assert message == "You can not buy that potion, as it is not being sold right now."
    assert updated_character["renown"] == 500
    assert updated_character["potions"] == []
    assert updated_potion_data[0]["shoplist"] == ["hp5", "damage1"]


def test_buy_character_potion_rejects_when_buyer_lacks_renown():
    potion_data = make_purchase_potion_data()
    character_data = {
        "name": "Test Hero",
        "renown": 100,
        "potions": [],
    }

    updated_character, updated_potion_data, message = buy_character_potion(
        character_data,
        potion_data,
        "hp5",
    )

    assert message == "You do not have enough renown to purchase this."
    assert updated_character["renown"] == 100
    assert updated_character["potions"] == []
    assert updated_potion_data[0]["shoplist"] == ["hp5", "damage1"]


def test_buy_character_potion_rejects_when_inventory_is_full():
    potion_data = make_purchase_potion_data()
    character_data = {
        "name": "Test Hero",
        "renown": 500,
        "potions": ["p1", "p2", "p3", "p4", "p5"],
    }

    updated_character, updated_potion_data, message = buy_character_potion(
        character_data,
        potion_data,
        "hp5",
    )

    assert message == "You do not have enough inventory space to own more potions."
    assert updated_character["renown"] == 500
    assert updated_character["potions"] == ["p1", "p2", "p3", "p4", "p5"]
    assert updated_potion_data[0]["shoplist"] == ["hp5", "damage1"]


def test_give_character_potion_transfers_potion_to_recipient():
    from src.potion_repository import give_character_potion

    gifter_data = {
        "name": "Alice",
        "potions": ["hp5", "hit1"],
    }
    gifted_data = {
        "name": "Bob",
        "potions": ["damage1"],
    }

    msg, gifter, gifted = give_character_potion(
        gifter_data,
        gifted_data,
        "hp5",
    )

    assert msg == "Alice has given Bob a potion of hp5"
    assert gifter == "Alice"
    assert gifted == "Bob"
    assert gifter_data["potions"] == ["hit1"]
    assert gifted_data["potions"] == ["damage1", "hp5"]


def test_give_character_potion_lowercases_item_before_transfer():
    from src.potion_repository import give_character_potion

    gifter_data = {
        "name": "Alice",
        "potions": ["hp5"],
    }
    gifted_data = {
        "name": "Bob",
        "potions": [],
    }

    msg, gifter, gifted = give_character_potion(
        gifter_data,
        gifted_data,
        "HP5",
    )

    assert msg == "Alice has given Bob a potion of hp5"
    assert gifter == "Alice"
    assert gifted == "Bob"
    assert gifter_data["potions"] == []
    assert gifted_data["potions"] == ["hp5"]


def test_give_character_potion_fails_when_sender_does_not_have_item():
    from src.potion_repository import give_character_potion

    gifter_data = {
        "name": "Alice",
        "potions": ["hit1"],
    }
    gifted_data = {
        "name": "Bob",
        "potions": ["damage1"],
    }

    msg, gifter, gifted = give_character_potion(
        gifter_data,
        gifted_data,
        "hp5",
    )

    assert msg == "You do not have this item to give."
    assert gifter == "Alice"
    assert gifted == "Bob"
    assert gifter_data["potions"] == ["hit1"]
    assert gifted_data["potions"] == ["damage1"]


def test_give_character_potion_fails_when_recipient_inventory_has_four_potions():
    from src.potion_repository import give_character_potion

    gifter_data = {
        "name": "Alice",
        "potions": ["hp5", "hit1"],
    }
    gifted_data = {
        "name": "Bob",
        "potions": ["damage1", "damage2", "ac1", "tstr1"],
    }

    msg, gifter, gifted = give_character_potion(
        gifter_data,
        gifted_data,
        "hp5",
    )

    assert msg == "You can not give Bob anything, as they have no space in their inventory to take this item."
    assert gifter == "Alice"
    assert gifted == "Bob"
    assert gifter_data["potions"] == ["hp5", "hit1"]
    assert gifted_data["potions"] == ["damage1", "damage2", "ac1", "tstr1"]


def test_give_character_potion_allows_transfer_when_recipient_inventory_has_three_potions():
    from src.potion_repository import give_character_potion

    gifter_data = {
        "name": "Alice",
        "potions": ["hp5"],
    }
    gifted_data = {
        "name": "Bob",
        "potions": ["damage1", "damage2", "ac1"],
    }

    msg, gifter, gifted = give_character_potion(
        gifter_data,
        gifted_data,
        "hp5",
    )

    assert msg == "Alice has given Bob a potion of hp5"
    assert gifter == "Alice"
    assert gifted == "Bob"
    assert gifter_data["potions"] == []
    assert gifted_data["potions"] == ["damage1", "damage2", "ac1", "hp5"]


def make_use_potion_character(**overrides):
    character_data = {
        "name": "Tester",
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
        "reset": 3,
        "remaining feats": 2,
        "total feats": 2,
        "traitdr": 0,
        "armordr": 0,
        "regeneration": 0,
    }
    character_data.update(overrides)
    return character_data


def test_use_character_potion_returns_unknown_potion_message_without_changes():
    character_data = make_use_potion_character(potions=["hit1"])

    updated_character, message = use_character_potion(
        character_data,
        "notapotion",
        None,
    )

    assert message == "You do not have a potion of notapotion"
    assert updated_character["potions"] == ["hit1"]


def test_use_character_potion_applies_temporary_hit_potion():
    character_data = make_use_potion_character(potions=["hit1"])

    updated_character, message = use_character_potion(
        character_data,
        "hit1",
        (1, "increasing hit chance by 1 for duration of fight"),
    )

    assert (
        message
        == "Tester drank a hit1 potion, [color=red]increasing hit chance by 1 for duration of fight[/color] for next match."
    )
    assert updated_character["potionhit"] == 1
    assert updated_character["potioneffect"] == "increasing hit chance by 1 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_damage_potion():
    character_data = make_use_potion_character(potions=["damage1"])

    updated_character, message = use_character_potion(
        character_data,
        "damage1",
        (1, "increasing damage by 1 for duration of fight"),
    )

    assert (
        message
        == "Testerdrank a damage1 potion, [color=red]increasing damage by 1 for duration of fight[/color] for next match."
    )
    assert updated_character["potiondamage"] == 1
    assert updated_character["potioneffect"] == "increasing damage by 1 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_ac_potion():
    character_data = make_use_potion_character(potions=["ac1"])

    updated_character, message = use_character_potion(
        character_data,
        "ac1",
        (1, "increasing armor class by 1 for duration of fight"),
    )

    assert (
        message
        == "Tester drank a ac1 potion, [color=red]increasing armor class by 1 for duration of fight[/color] for next match."
    )
    assert updated_character["potionac"] == 1
    assert updated_character["potioneffect"] == "increasing armor class by 1 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_strength_potion():
    character_data = make_use_potion_character(potions=["tstr1"])

    updated_character, message = use_character_potion(
        character_data,
        "tstr1",
        (1, "increasing strength by 1 for duration of fight"),
    )

    assert (
        message
        == "Tester drank a tstr1 potion, [color=red]increasing strength by 1 for duration of fight[/color] for next match."
    )
    assert updated_character["potionstr"] == 1
    assert updated_character["potioneffect"] == "increasing strength by 1 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_dexterity_potion():
    character_data = make_use_potion_character(potions=["tdex1"])

    updated_character, message = use_character_potion(
        character_data,
        "tdex1",
        (1, "increasing dexterity by 1 for duration of fight"),
    )

    assert (
        message
        == "Tester drank a tdex1 potion, [color=red]increasing dexterity by 1 for duration of fight[/color] for next match."
    )
    assert updated_character["potiondex"] == 1
    assert updated_character["potioneffect"] == "increasing dexterity by 1 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_constitution_potion():
    character_data = make_use_potion_character(potions=["tcon1"])

    updated_character, message = use_character_potion(
        character_data,
        "tcon1",
        (1, "increasing constitution by 1 for duration of fight"),
    )

    assert (
        message
        == "Tester drank a tcon1 potion, [color=red]increasing constitution by 1 for duration of fight[/color] for next match."
    )
    assert updated_character["potioncon"] == 1
    assert updated_character["potioneffect"] == "increasing constitution by 1 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_hp_potion():
    character_data = make_use_potion_character(potions=["hp5"])

    updated_character, message = use_character_potion(
        character_data,
        "hp5",
        (5, "increasing hp by 5 for duration of fight"),
    )

    assert (
        message
        == "Tester drank a hp5 potion, [color=red]increasing hp by 5 for duration of fight[/color] for next match."
    )
    assert updated_character["potionhp"] == 5
    assert updated_character["potioneffect"] == "increasing hp by 5 for duration of fight"
    assert updated_character["potions"] == []


def test_use_character_potion_applies_temporary_blur_potion():
    character_data = make_use_potion_character(
        potions=["blur1"],
        potionblur=2,
    )

    updated_character, message = use_character_potion(
        character_data,
        "blur1",
        (1, "gives 1% chance to negate opponent's damage"),
    )

    assert (
        message
        == "Tester drank a blur1 potion, [color=red]gives 1% chance to negate opponent's damage for next match."
    )
    assert updated_character["potionblur"] == 3
    assert updated_character["potioneffect"] == "gives 1% chance to negate opponent's damage"
    assert updated_character["potions"] == []


def test_use_character_potion_blocks_temporary_potion_when_effect_is_active():
    character_data = make_use_potion_character(
        potions=["hit1"],
        potioneffect="existing effect",
    )

    updated_character, message = use_character_potion(
        character_data,
        "hit1",
        (1, "increasing hit chance by 1 for duration of fight"),
    )

    assert message == "You already have a potion in effect."
    assert updated_character["potionhit"] == 0
    assert updated_character["potioneffect"] == "existing effect"
    assert updated_character["potions"] == ["hit1"]


def test_use_character_potion_applies_valid_permanent_strength_progression():
    character_data = make_use_potion_character(
        potions=["str1"],
        pstrength=0,
    )

    updated_character, message = use_character_potion(
        character_data,
        "str1",
        (1, "permanently increases strength by 1"),
    )

    assert message == "Tester drank a str1 potion, obtaining a permanent [color=red] +1 to strength[/color]"
    assert updated_character["pstrength"] == 1
    assert updated_character["potions"] == []


def test_use_character_potion_rejects_invalid_permanent_strength_progression():
    character_data = make_use_potion_character(
        potions=["str2"],
        pstrength=0,
    )

    updated_character, message = use_character_potion(
        character_data,
        "str2",
        (2, "permanently increases strength by 1"),
    )

    assert message == "You can not drink this potion, as it is either too powerful or too weak to use right now."
    assert updated_character["pstrength"] == 0
    assert updated_character["potions"] == ["str2"]


def test_use_character_potion_respec_increments_reset_and_removes_potion():
    character_data = make_use_potion_character(
        potions=["respec"],
        reset=3,
    )

    updated_character, message = use_character_potion(
        character_data,
        "respec",
        (1, "allows to respec character"),
    )

    assert (
        message
        == "Tester drank a respec potion. Allowing them a chance to change their feats, traits, and stat points."
    )
    assert updated_character["reset"] == 4
    assert updated_character["potions"] == []


def test_use_character_potion_stimulant_adds_feat_slots_and_removes_potion():
    character_data = make_use_potion_character(
        potions=["stimulant"],
        **{
            "remaining feats": 2,
            "total feats": 2,
        },
    )

    updated_character, message = use_character_potion(
        character_data,
        "stimulant",
        (1, "Allows one to learn a new feat they meet requirements for"),
    )

    assert message == "Tester drank a stimulant potion. Allowing them to learn a new feat they qualify for."
    assert updated_character["remaining feats"] == 3
    assert updated_character["total feats"] == 3
    assert updated_character["potions"] == []


def test_use_character_potion_regen_preserves_legacy_inventory_bug():
    character_data = make_use_potion_character(
        potions=["regen1"],
        traitdr=0,
        armordr=0,
        regeneration=0,
    )

    updated_character, message = use_character_potion(
        character_data,
        "regen1",
        (1, "grants +1 regeneration for duration of fight"),
    )

    assert (
        message
        == "Tester drank a regen1 potion, [color=red]grants +1 regeneration for duration of fight for next match."
    )
    assert updated_character["potionregen"] == 1
    assert updated_character["potioneffect"] == "grants +1 regeneration for duration of fight"
    assert updated_character["potions"] == ["regen1"]


def test_use_character_potion_valid_potion_missing_from_inventory_raises_value_error():
    character_data = make_use_potion_character(potions=[])

    try:
        use_character_potion(
            character_data,
            "hit1",
            (1, "increasing hit chance by 1 for duration of fight"),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when valid potion is missing from inventory.")


def test_use_character_potion_applies_strength_progression():
    character_data = make_use_potion_character(
        potions=["str1"],
        pstrength=0,
    )

    updated_character, message = use_character_potion(
        character_data,
        "str1",
        [1, "permanently increases strength by 1"],
    )

    assert message == "Tester drank a str1 potion, obtaining a permanent [color=red] +1 to strength[/color]"
    assert updated_character["pstrength"] == 1
    assert "str1" not in updated_character["potions"]


def test_use_character_potion_rejects_strength_progression_if_previous_tier_missing():
    character_data = make_use_potion_character(
        potions=["str2"],
        pstrength=0,
    )

    updated_character, message = use_character_potion(
        character_data,
        "str2",
        [2, "permanently increases strength by 1"],
    )

    assert message == "You can not drink this potion, as it is either too powerful or too weak to use right now."
    assert updated_character["pstrength"] == 0
    assert "str2" in updated_character["potions"]


def test_use_character_potion_applies_dexterity_progression():
    character_data = make_use_potion_character(
        potions=["dex3"],
        pdexterity=2,
    )

    updated_character, message = use_character_potion(
        character_data,
        "dex3",
        [3, "permanently increases dexterity by 1"],
    )

    assert message == "Tester drank a dex3 potion, obtaining a permanent [color=red] +1 to dexterity[/color]"
    assert updated_character["pdexterity"] == 3
    assert "dex3" not in updated_character["potions"]


def test_use_character_potion_applies_constitution_progression():
    character_data = make_use_potion_character(
        potions=["con5"],
        pconstitution=4,
    )

    updated_character, message = use_character_potion(
        character_data,
        "con5",
        [5, "permanently increases constitution by 1"],
    )

    assert message == "Tester drank a con5 potion, obtaining a permanent [color=red] +1 to constitution[/color]"
    assert updated_character["pconstitution"] == 5
    assert "con5" not in updated_character["potions"]