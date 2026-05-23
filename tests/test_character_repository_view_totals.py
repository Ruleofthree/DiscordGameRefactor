from src.character_repository import calculate_character_view_totals


def base_character_data(**overrides):
    data = {
        "build": "strength",
        "hp": 20,
        "hit": 3,
        "damage": 2,
        "ac": 10,

        "strength": 8,
        "dexterity": 6,
        "constitution": 4,

        "pstrength": 0,
        "pdexterity": 0,
        "pconstitution": 0,

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
    }
    data.update(overrides)
    return data


def test_calculate_character_view_totals_for_strength_build_preserves_legacy_math():
    char_data = base_character_data(build="strength")

    result = calculate_character_view_totals(char_data)

    assert result["strength"] == 8
    assert result["dexterity"] == 6
    assert result["constitution"] == 4
    assert result["thit"] == 7
    assert result["tdamage"] == 7
    assert result["thp"] == 30
    assert result["tac"] == 15
    assert result["tdr"] == 0
    assert result["regeneration"] == 0
    assert result["blur"] == 0
    assert result["initiative"] == 3


def test_calculate_character_view_totals_for_dexterity_build_preserves_legacy_math():
    char_data = base_character_data(build="dexterity")

    result = calculate_character_view_totals(char_data)

    assert result["thp"] == 30
    assert result["thit"] == 7
    assert result["tdamage"] == 4
    assert result["tac"] == 13


def test_calculate_character_view_totals_for_constitution_build_preserves_legacy_math():
    char_data = base_character_data(build="constitution")

    result = calculate_character_view_totals(char_data)

    assert result["thp"] == 26
    assert result["thit"] == 8
    assert result["tdamage"] == 4
    assert result["tac"] == 17


def test_calculate_character_view_totals_includes_potion_armor_trait_and_cursed_values():
    char_data = base_character_data(
        build="strength",
        pstrength=1,
        pdexterity=2,
        pconstitution=3,
        potionstr=1,
        potiondex=1,
        potioncon=1,
        potionhp=5,
        potionregen=2,
        potionblur=3,
        armorstrength=2,
        armordexterity=1,
        armorconstitution=2,
        armorhit=4,
        armordamage=5,
        armorac=6,
        armorhp=7,
        armordr=8,
        armorblur=9,
        armorinitiative=10,
        feathp=11,
        feathit=12,
        featdamage=13,
        featac=14,
        traithit=15,
        traitdamage=16,
        traitac=17,
        traitdr=18,
        traithp=19,
        traitregen=20,
        cursed=5,
        blur=21,
    )

    result = calculate_character_view_totals(char_data)

    assert result["strength"] == 12
    assert result["dexterity"] == 10
    assert result["constitution"] == 10
    assert result["thit"] == 35
    assert result["tdamage"] == 39
    assert result["thp"] == 87
    assert result["tac"] == 49
    assert result["tdr"] == 26
    assert result["regeneration"] == 22
    assert result["blur"] == 33
    assert result["initiative"] == 15