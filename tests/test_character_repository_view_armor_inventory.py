from src.character_repository import format_character_view_armor_inventory


def test_format_character_view_armor_inventory_returns_na_for_empty_slots():
    char_data = {
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        }
    }

    result = format_character_view_armor_inventory(char_data)

    assert result == ("n/a", "n/a", "n/a")


def test_format_character_view_armor_inventory_formats_first_slot_and_preserves_legacy_mutation():
    char_data = {
        "armor": {
            "armor1": ["Iron Armor", "+1 AC", 1000],
            "armor2": "n/a",
            "armor3": "n/a",
        }
    }

    result = format_character_view_armor_inventory(char_data)

    assert result[0] == "Iron Armor, +1 AC Selling Value: [color=yellow]500[/color] renown"
    assert result[1] == "n/a"
    assert result[2] == "n/a"

    assert char_data["armor"]["armor1"] == ["Iron Armor", "+1 AC"]


def test_format_character_view_armor_inventory_formats_all_three_slots_with_legacy_second_slot_typo():
    char_data = {
        "armor": {
            "armor1": ["Iron Armor", "+1 AC", 1000],
            "armor2": ["Leather Armor", "+1 Dex", 750],
            "armor3": ["Steel Armor", "+2 HP", 300],
        }
    }

    result = format_character_view_armor_inventory(char_data)

    assert result[0] == "Iron Armor, +1 AC Selling Value: [color=yellow]500[/color] renown"
    assert result[1] == "Leather Armor, +1 Dex Selling Value: [color=yellow]375[/color] rewnown"
    assert result[2] == "Steel Armor, +2 HP Selling Value: [color=yellow]150[/color] renown"

    assert char_data["armor"]["armor1"] == ["Iron Armor", "+1 AC"]
    assert char_data["armor"]["armor2"] == ["Leather Armor", "+1 Dex"]
    assert char_data["armor"]["armor3"] == ["Steel Armor", "+2 HP"]