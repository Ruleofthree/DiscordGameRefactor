from src.character_repository import apply_character_view_totals


def test_apply_character_view_totals_updates_view_total_fields():
    char_data = {
        "thp": 0,
        "tac": 0,
        "tdr": 0,
        "thit": 0,
        "tdamage": 0,
        "initiative": 0,
        "regeneration": 0,
    }

    totals = {
        "thp": 35,
        "tac": 16,
        "tdr": 2,
        "thit": 7,
        "tdamage": 8,
        "initiative": 4,
        "regeneration": 3,
    }

    result = apply_character_view_totals(char_data, totals)

    assert result == char_data
    assert char_data["thp"] == 35
    assert char_data["tac"] == 16
    assert char_data["tdr"] == 2
    assert char_data["thit"] == 7
    assert char_data["tdamage"] == 8
    assert char_data["initiative"] == 4
    assert char_data["regeneration"] == 3


def test_apply_character_view_totals_preserves_unrelated_fields():
    char_data = {
        "name": "Test Character",
        "level": 3,
        "renown": 50,
        "thp": 0,
        "tac": 0,
        "tdr": 0,
        "thit": 0,
        "tdamage": 0,
        "initiative": 0,
        "regeneration": 0,
    }

    totals = {
        "thp": 35,
        "tac": 16,
        "tdr": 2,
        "thit": 7,
        "tdamage": 8,
        "initiative": 4,
        "regeneration": 3,
    }

    apply_character_view_totals(char_data, totals)

    assert char_data["name"] == "Test Character"
    assert char_data["level"] == 3
    assert char_data["renown"] == 50