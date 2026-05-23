import pytest
from src.trait_repository import (
    get_trait,
    get_trait_dictionary,
    get_trait_dictionary_and_names,
    get_trait_names,
)

def test_get_trait_dictionary_returns_trait_dict():
    result = get_trait_dictionary()

    assert isinstance(result, dict)
    assert "regeneration" in result
    assert "brawler" in result
    assert "cursed" in result


def test_get_trait_names_returns_trait_names():
    result = get_trait_names()

    assert isinstance(result, list)
    assert "regeneration" in result
    assert "brawler" in result
    assert "cursed" in result

def test_get_trait_dictionary_and_names_returns_legacy_shape():
    trait_dictionary, trait_names = get_trait_dictionary_and_names()

    assert isinstance(trait_dictionary, list)
    assert isinstance(trait_dictionary[0], dict)
    assert isinstance(trait_names, list)
    assert trait_names == list(trait_dictionary[0].keys())


def test_get_trait_returns_single_traits_entry():
    result = get_trait("regeneration")

    assert isinstance(result, dict)
    assert result["desc"] == "Gain +2 Regeneration at level 1 and an additional +1 at 5, 10, 15, and 20"
    assert result["bonus"] == [2, 3, 4, 5, 6]


def test_get_trait_raises_keyerror_for_invalid_trait():
    with pytest.raises(KeyError):
        get_trait("not a real trait")


