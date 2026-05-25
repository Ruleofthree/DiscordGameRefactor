import random

from src.data_loader import load_potions


POTION_RARITY_ORDER = ("common", "uncommon", "rare", "vrare", "relic")


def get_potion_dictionary():
    return load_potions()


def get_potion_data():
    return load_potions()[0]


def get_potion_shop_lists():
    potion_data = get_potion_data()

    return tuple(
        list(potion_data[rarity].keys())
        for rarity in POTION_RARITY_ORDER
    )


def find_potion(potion_name):
    potion_data = get_potion_data()

    for rarity in POTION_RARITY_ORDER:
        if potion_name in potion_data[rarity]:
            return rarity, potion_data[rarity][potion_name]

    return None


def get_potion_price(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[0]


def get_potion_description(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[1]


def get_potion_effect_value(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[2]


def get_potion_sell_value(potion_name):
    price = get_potion_price(potion_name)

    if price is None:
        return None

    return int(price / 2)


def get_potion_effect_info(potion_name):
    result = find_potion(potion_name)

    if result is None:
        return None

    _, potion_info = result
    return potion_info[2], potion_info[1]


def sell_character_potion(character_data, potion_name):
    """
    Sell one potion from a character inventory.

    This preserves the legacy pri_11_sellpotion message behavior while keeping
    file loading and saving in the legacy wrapper for now.
    """
    if potion_name not in character_data["potions"]:
        return character_data, "You do not have that potion to sell."

    half_price = get_potion_sell_value(potion_name)

    if half_price is None:
        return character_data, "That potion does not exist in the potion data."

    character_data["renown"] += half_price
    character_data["potions"].remove(potion_name)

    message = (
        character_data["name"]
        + " has sold a [color=red]"
        + potion_name
        + "[/color] for [color=yellow]"
        + str(half_price)
        + " renown[/color]."
    )

    return character_data, message


def stock_potion_shop(
    potion_dictionary,
    common_list,
    uncommon_list,
    rare_list,
    very_rare_list,
    relic_list,
):
    """
    Stock the potion shop with 20 potions.

    This preserves the legacy pri_10_stockpotion rarity thresholds and index
    selection behavior while keeping file writing in the legacy wrapper.
    """
    potion_dictionary[0]["shoplist"] = []

    for _ in range(1, 21):
        number = random.randint(1, 100)

        if number in range(98, 101):
            relic_potion = len(relic_list)
            index = random.randint(1, relic_potion - 1)
            chosen_potion = relic_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(90, 98):
            very_rare_potion = len(very_rare_list)
            index = random.randint(1, very_rare_potion - 1)
            chosen_potion = very_rare_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(77, 90):
            rare_potion = len(rare_list)
            index = random.randint(1, rare_potion - 1)
            chosen_potion = rare_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(51, 77):
            uncommon_potion = len(uncommon_list)
            index = random.randint(1, uncommon_potion - 1)
            chosen_potion = uncommon_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

        elif number in range(1, 51):
            common_potion = len(common_list)
            index = random.randint(1, common_potion - 1)
            chosen_potion = common_list[index]
            potion_dictionary[0]["shoplist"].append(chosen_potion)

    shop_string = ", ".join(potion_dictionary[0]["shoplist"])
    msg = "Shop stocked for the week as follows: \n" + shop_string

    return potion_dictionary, msg, shop_string


def get_potion_price_from_data(potion_data, potion_name):
    """
    Return a potion price from caller-provided potion data.

    This preserves the legacy category search order without loading potions.json
    inside the deterministic purchase helper.
    """
    for rarity in POTION_RARITY_ORDER:
        if potion_name in potion_data[0][rarity]:
            return potion_data[0][rarity][potion_name][0]

    return None


def buy_character_potion(character_data, potion_data, potion_name):
    """
    Buy one potion from the current potion shop.

    This preserves pri_10_buypotion state mutation while keeping file loading
    and saving in the legacy wrapper.
    """
    potion_list = potion_data[0]["shoplist"]

    if potion_name not in potion_list:
        return (
            character_data,
            potion_data,
            "You can not buy that potion, as it is not being sold right now.",
        )

    price = get_potion_price_from_data(potion_data, potion_name)

    if price <= character_data["renown"]:
        if len(character_data["potions"]) >= 5:
            message = "You do not have enough inventory space to own more potions."
        else:
            character_data["renown"] -= price
            potion_data[0]["shoplist"].remove(potion_name)
            character_data["potions"].append(potion_name)
            message = character_data["name"] + " has puchased a potion of " + potion_name + "."
    else:
        message = "You do not have enough renown to purchase this."

    return character_data, potion_data, message