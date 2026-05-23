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