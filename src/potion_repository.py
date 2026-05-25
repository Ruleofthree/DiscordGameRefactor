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