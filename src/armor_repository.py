from src.data_loader import load_armor

import random


def get_armor_dictionary():
    """
    Return the raw armor data loaded from armor.json

    The current armor.json file is stored as a list containing one dictionary.
    This preserves that legacy shape for now.
    """
    return load_armor()


def get_armor_shop_lists():
    """
    Return armor shop category list in the same order as the legacy armorShop() function.

    Lecasy return order:
    cat1 common, cat1 uncommon, cat1 rare,
    cat2 common, cat2 uncommon, cat2 rare,
    cat3 common, cat3 uncommon, cat3 rare
    """
    armor_dictionary = get_armor_dictionary()
    armor_data = armor_dictionary[0]

    cat_one_common_list = list(armor_data["cat1"]["common"].keys())
    cat_one_uncommon_list = list(armor_data["cat1"]["uncommon"].keys())
    cat_one_rare_list = list(armor_data["cat1"]["rare"].keys())

    cat_two_common_list = list(armor_data["cat2"]["common"].keys())
    cat_two_uncommon_list = list(armor_data["cat2"]["uncommon"].keys())
    cat_two_rare_list = list(armor_data["cat2"]["rare"].keys())

    cat_three_common_list = list(armor_data["cat3"]["common"].keys())
    cat_three_uncommon_list = list(armor_data["cat3"]["uncommon"].keys())
    cat_three_rare_list = list(armor_data["cat3"]["rare"].keys())

    return(
        cat_one_common_list,
        cat_one_uncommon_list,
        cat_one_rare_list,
        cat_two_common_list,
        cat_two_uncommon_list,
        cat_two_rare_list,
        cat_three_common_list,
        cat_three_uncommon_list,
        cat_three_rare_list
    )


def get_armor_effects(armor_key):
    """
    Return the effect keys attached to a specific armor entry.

    Example:
    armor4 -> ["dex2", "ac2"]
    """
    armor_dictionary = get_armor_dictionary()
    armor_data = armor_dictionary[0]

    return armor_data["armorlist"][armor_key]


def calculate_armor_effect_price(effect_key, armor_dictionary=None):
    """
    Return the renown price for one armor effect key.

    This preserves the legacy armor category lookup behavior while keeping
    price calculation out of the legacy private-command wrapper.
    """
    if armor_dictionary is None:
        armor_dictionary = get_armor_dictionary()

    armor_data = armor_dictionary[0]

    for category_name in ("cat1", "cat2", "cat3"):
        for rarity_name in ("common", "uncommon", "rare"):
            category = armor_data[category_name][rarity_name]
            if effect_key in category:
                return category[effect_key][0]

    raise KeyError(effect_key)


def calculate_armor_item_price(armor_item, armor_dictionary=None):
    """
    Return the total renown price for one armor shop item.

    Sold armor displays as 0 renown in the legacy shop output.
    """
    if armor_dictionary is None:
        armor_dictionary = get_armor_dictionary()

    if armor_item == "sold":
        return 0

    price = 0
    for effect_key in armor_item:
        price += calculate_armor_effect_price(effect_key, armor_dictionary)

    return price


def buy_character_armor(char_sheet, armor_data, armor):
    if armor not in armor_data[0]["armorlist"]:
        msg = "You seemed to have not typed in your desired choice correctly."
        return char_sheet, armor_data, msg

    choice = armor_data[0]["armorlist"][armor]

    if choice == "sold":
        msg = "This armor has already been sold."
        return char_sheet, armor_data, msg

    armor_string = ", ".join(choice)
    price = calculate_armor_item_price(choice, armor_data)

    inventory_slots = list(char_sheet["armor"].keys())
    armor1 = inventory_slots[0]
    armor2 = inventory_slots[1]
    armor3 = inventory_slots[2]

    if price <= char_sheet["renown"]:
        if (
            char_sheet["armor"][armor1] != "n/a"
            and char_sheet["armor"][armor2] != "n/a"
            and char_sheet["armor"][armor3] != "n/a"
        ):
            msg = "You do not have enough inventory space to own more armor."
        else:
            char_sheet["renown"] -= price
            armor_data[0]["armorlist"][armor] = "sold"

            purchased_armor = list(choice)
            purchased_armor.append(price)

            if char_sheet["armor"][armor1] == "n/a":
                char_sheet["armor"][armor1] = purchased_armor
            elif char_sheet["armor"][armor2] == "n/a":
                char_sheet["armor"][armor2] = purchased_armor
            elif char_sheet["armor"][armor3] == "n/a":
                char_sheet["armor"][armor3] = purchased_armor

            msg = (
                char_sheet["name"]
                + " has purchased an armor of [color=red]"
                + armor_string
                + "[/color]."
            )
    else:
        msg = "You do not have enough renown to purchase this."

    return char_sheet, armor_data, msg


def sell_character_armor(char_sheet, armor_key, character):
    if armor_key in char_sheet["armor"]:
        if armor_key in char_sheet["equip"]:
            msg = "You can't sell armor that is currently equipped."
        else:
            price = int(char_sheet["armor"][armor_key][-1] / 2)
            char_sheet["renown"] += price
            char_sheet["armor"][armor_key] = "n/a"

            if "armor1" not in char_sheet["armor"]:
                char_sheet["armor"]["armor1"] = char_sheet["armor"].pop(armor_key)
            elif "armor2" not in char_sheet["armor"]:
                char_sheet["armor"]["armor2"] = char_sheet["armor"].pop(armor_key)
            elif "armor3" not in char_sheet["armor"]:
                char_sheet["armor"]["armor3"] = char_sheet["armor"].pop(armor_key)

            msg = character + " sold some armor for [color=yellow] " + str(price) + " renown[/color]"
    else:
        msg = "You do not have that armor to sell."

    return char_sheet, msg


def rename_character_armor(character_data, armor_name, armor_remove):
    if armor_remove not in character_data["armor"].keys():
        return (
            armor_remove
            + " is not within your inventory to rename. Please check you are typing armor name correctly,"
            + " then try this command again"
        )

    if armor_name in character_data["armor"].keys():
        return (
            "You already have a piece of armor named "
            + armor_name
            + ". Please use a new name, and try this command "
            + "again"
        )

    if armor_remove == character_data["equip"]:
        return "You need to unequip the armor first, before using this command."

    if character_data["armor"][armor_remove] != "n/a":
        character_data["armor"][armor_name] = character_data["armor"].pop(armor_remove)
        return character_data["name"] + " renamed " + armor_remove + " to " + armor_name + "."

    return "There is no armor in that slot to rename. Please double check inventory, then use this command again."


def unequip_character_armor(character_data, armor):
    character_data["equip"] = ""
    msg = character_data["name"] + " has unequipped " + armor

    character_data["armorhit"] = 0
    character_data["armordamage"] = 0
    character_data["armorac"] = 0
    character_data["armorhp"] = 0
    character_data["armordr"] = 0
    character_data["armorinitiative"] = 0
    character_data["armorstrength"] = 0
    character_data["armordexterity"] = 0
    character_data["armorconstitution"] = 0
    character_data["armorblur"] = 0

    return msg


def build_armor_shop_display(armor_shop_items, armor_dictionary=None):
    """
    Build the legacy armor shop display string.

    This preserves the exact F-list color-tag format used by pri_10_armorshop().
    """
    if armor_dictionary is None:
        armor_dictionary = get_armor_dictionary()

    armor_prices = [
        calculate_armor_item_price(armor_item, armor_dictionary)
        for armor_item in armor_shop_items
    ]

    shop_list = {}
    num = 1
    for armor_item in armor_shop_items:
        shop_list["Armor" + str(num)] = armor_item
        num += 1

    flattened_items = []
    for key in shop_list:
        flattened_items.append(key)
        flattened_items.append(shop_list[key])

    armor_list = "\n".join(
        "{} [color=red]{}[/color]: [color=yellow]({} renown)[/color]".format(*item)
        for item in zip(flattened_items[0::2], flattened_items[1::2], armor_prices[0:])
    )

    return armor_list


def stock_armor_shop(
    armor_dictionary,
    cat_one_common_list,
    cat_one_uncommon_list,
    cat_one_rare_list,
    cat_two_common_list,
    cat_two_uncommon_list,
    cat_two_rare_list,
    cat_three_common_list,
    cat_three_uncommon_list,
    cat_three_rare_list,
):
    """
    Stock the armor shop with 20 armor entries.

    This preserves the legacy pri_11_stockarmor random threshold behavior while
    keeping armor.json file writing in the legacy wrapper.
    """
    for num in range(1, 21):
        rand = random.randint(1, 100)

        if rand in range(1, 101):
            category = random.randint(1, 100)

            if category in range(80, 101):
                item = []
                random_attribute = random.choice(cat_one_rare_list)
                item.append(random_attribute)

            if category in range(46, 80):
                item = []
                random_attribute = random.choice(cat_one_uncommon_list)
                item.append(random_attribute)

            if category in range(1, 46):
                item = []
                random_attribute = random.choice(cat_one_common_list)
                item.append(random_attribute)

        if rand in range(1, 41):
            category = random.randint(1, 100)

            if category in range(86, 101):
                random_attribute = random.choice(cat_two_rare_list)
                item.append(random_attribute)

            if category in range(51, 86):
                random_attribute = random.choice(cat_two_uncommon_list)
                item.append(random_attribute)

            if category in range(1, 51):
                random_attribute = random.choice(cat_two_common_list)
                item.append(random_attribute)

        if rand in range(1, 11):
            category = random.randint(1, 100)

            if category in range(86, 101):
                random_attribute = random.choice(cat_three_rare_list)
                item.append(random_attribute)

            elif category in range(51, 86):
                random_attribute = random.choice(cat_three_uncommon_list)
                item.append(random_attribute)

            elif category in range(1, 51):
                random_attribute = random.choice(cat_three_common_list)
                item.append(random_attribute)

        armor_dictionary[0]["armorlist"]["armor" + str(num)] = item

    msg = "Armor Shop has been stocked for the week."

    return armor_dictionary, msg