from src.character_repository import build_character_view_context


def make_character_data():
    return {
        "equip": "n/a",
        "name": "Test Character",
        "trait": "brawler",
        "level": 1,
        "total feats": 2,
        "base damage": "1d10",
        "renown": 100,
        "currentxp": 25,
        "nextlevel": 100,
        "remaining feats": 1,
        "feats taken": ["focus", "power attack"],
        "ap": 15,
        "reset": 3,
        "wins": 2,
        "losses": 1,
        "forfeits": 0,
        "potioneffect": "none",

        "build": "strength",
        "hp": 20,
        "hit": 3,
        "damage": 2,
        "ac": 10,

        "strength": 8,
        "dexterity": 6,
        "constitution": 4,

        "pstrength": 1,
        "pdexterity": 2,
        "pconstitution": 3,

        "potionstr": 0,
        "potiondex": 0,
        "potioncon": 0,
        "potionhp": 0,
        "potionregen": 0,
        "potionblur": 0,

        "armorstrength": 0,
        "armordexterity": 0,
        "armorconstitution": 0,
        "armorhit": 0,
        "armordamage": 0,
        "armorac": 0,
        "armorhp": 0,
        "armordr": 0,
        "armorblur": 0,
        "armorinitiative": 0,

        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,

        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traitdr": 0,
        "traithp": 0,
        "traitregen": 0,

        "cursed": 0,
        "blur": 0,

        "thp": 0,
        "tac": 0,
        "tdr": 0,
        "thit": 0,
        "tdamage": 0,

        "armor": {
            "armor1": ["Iron Armor", "+1 AC", 1000],
            "armor2": "n/a",
            "armor3": "n/a",
        },

        "potions": ["hp5", "damage1"],
    }


def test_build_character_view_context_includes_calculated_totals():
    char_data = make_character_data()

    result = build_character_view_context(char_data)

    assert result["totals"]["strength"] == 9
    assert result["totals"]["dexterity"] == 8
    assert result["totals"]["constitution"] == 7
    assert result["totals"]["thit"] == 7
    assert result["totals"]["tdamage"] == 8
    assert result["totals"]["thp"] == 35
    assert result["totals"]["tac"] == 16


def test_build_character_view_context_includes_armor_display_values():
    char_data = make_character_data()

    result = build_character_view_context(char_data)

    assert result["armor_one"] == "armor1"
    assert result["armor_two"] == "armor2"
    assert result["armor_three"] == "armor3"
    assert result["armor_inv_one"] == "Iron Armor, +1 AC Selling Value: [color=yellow]500[/color] renown"
    assert result["armor_inv_two"] == "n/a"
    assert result["armor_inv_three"] == "n/a"


def test_build_character_view_context_includes_potion_inventory_display():
    char_data = make_character_data()

    result = build_character_view_context(char_data)

    assert result["potion_inventory"] == "hp5, damage1"


def test_build_character_view_context_preserves_legacy_armor_mutation():
    char_data = make_character_data()

    build_character_view_context(char_data)

    assert char_data["armor"]["armor1"] == ["Iron Armor", "+1 AC"]
    

def test_build_character_view_context_includes_basic_display_fields():
    char_data = make_character_data()

    result = build_character_view_context(char_data)

    assert result["equip"] == "n/a"
    assert result["name"] == "Test Character"
    assert result["build"] == "strength"
    assert result["trait"] == "brawler"
    assert result["level"] == 1
    assert result["total_feats"] == 2
    assert result["base_damage"] == "1d10"
    assert result["renown"] == 100
    assert result["current_xp"] == 25
    assert result["next_level"] == 100
    assert result["remaining_feats"] == 1
    assert result["feats_taken"] == "focus, power attack"
    assert result["ap"] == 15
    assert result["reset"] == 3
    assert result["wins"] == 2
    assert result["losses"] == 1
    assert result["forfeits"] == 0
    assert result["potion_effect"] == "none"
    assert result["permanent_strength"] == 1
    assert result["permanent_dexterity"] == 2
    assert result["permanent_constitution"] == 3