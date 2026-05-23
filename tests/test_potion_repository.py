from src.potion_repository import (
    POTION_RARITY_ORDER,
    get_potion_dictionary,
    get_potion_shop_lists,
)


def test_get_potion_dictionary_returns_loaded_potions():
    potion_dictionary = get_potion_dictionary()

    assert isinstance(potion_dictionary, list)
    assert isinstance(potion_dictionary[0], dict)
    assert "common" in potion_dictionary[0]
    assert "uncommon" in potion_dictionary[0]
    assert "rare" in potion_dictionary[0]
    assert "vrare" in potion_dictionary[0]
    assert "relic" in potion_dictionary[0]


def test_get_potion_shop_lists_returns_legacy_shape():
    result = get_potion_shop_lists()

    assert isinstance(result, tuple)
    assert len(result) == 5

    common_list, uncommon_list, rare_list, vrare_list, relic_list = result

    assert "hp5" in common_list
    assert "hp15" in uncommon_list
    assert "hp25" in rare_list
    assert "damage5" in vrare_list
    assert "stimulant" in relic_list


def test_get_potion_shop_lists_matches_rarity_order():
    potion_dictionary = get_potion_dictionary()
    potion_data = potion_dictionary[0]

    result = get_potion_shop_lists()

    for rarity, potion_list in zip(POTION_RARITY_ORDER, result):
        assert potion_list == list(potion_data[rarity].keys())
