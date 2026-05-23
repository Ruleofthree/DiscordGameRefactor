import pytest

from src.armor_repository import (
    get_armor_dictionary,
    get_armor_effects,
    get_armor_shop_lists,
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