import pytest
from src.feat_repository import (
    get_feat,
    get_feat_action,
    get_feat_dictionary,
    get_feat_names,
    has_feat,
)


def test_get_feat_dictionary_returns_dictionary():
    result = get_feat_dictionary()

    assert isinstance(result, dict)
    assert "power attack" in result
    assert "true strike" in result


def test_get_feat_names_returns_list_of_feat_names():
    result = get_feat_names()

    assert isinstance(result, list)
    assert "power attack" in result
    assert "true strike" in result


def test_has_feat_returns_true_for_existing_feat():
    result = has_feat("power attack")

    assert result is True


def test_has_feat_returns_false_for_missing_feat():
    result = has_feat("fake test")

    assert result is False


def test_get_feat_returns_expected_feat_data():
    result = get_feat("power attack")

    assert result["stat"] == "strength"
    assert result["status"] == "passive"
    assert result["requirements"] == [1, 0, 0, 0, "none", 0,]


def test_get_feat_raises_key_error_for_missing_feat():
    with pytest.raises(KeyError):
        get_feat("fake test")


def test_get_feat_action_returns_action_field():
    result = get_feat_action("power attack")

    assert result == [1, 2, 3, 4, 5]