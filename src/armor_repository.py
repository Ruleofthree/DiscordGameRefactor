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