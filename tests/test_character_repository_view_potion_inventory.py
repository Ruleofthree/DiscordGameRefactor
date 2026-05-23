from src.character_repository import format_character_view_potion_inventory


def test_format_character_view_potion_inventory_returns_empty_string_for_no_potions():
    char_data = {
        "potions": []
    }

    result = format_character_view_potion_inventory(char_data)

    assert result == ""


def test_format_character_view_potion_inventory_joins_single_potion():
    char_data = {
        "potions": ["hp5"]
    }

    result = format_character_view_potion_inventory(char_data)

    assert result == "hp5"


def test_format_character_view_potion_inventory_joins_multiple_potions_with_comma_space():
    char_data = {
        "potions": ["hp5", "damage1", "ac1"]
    }

    result = format_character_view_potion_inventory(char_data)

    assert result == "hp5, damage1, ac1"