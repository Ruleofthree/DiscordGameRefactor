from src.data_loader import load_potions

POTION_RARITY_ORDER = ("common", "uncommon", "rare", "vrare", "relic")


def get_potion_dictionary():
    return load_potions()


def get_potion_shop_lists():
    potion_dictionary = load_potions()
    potion_data = potion_dictionary[0]

    return tuple(
        list(potion_data[rarity].keys())
        for rarity in POTION_RARITY_ORDER
    )