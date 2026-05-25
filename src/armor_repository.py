from src.data_loader import load_armor


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