import json

from original.onPRIUtils import pri_6_trait


def make_character_file(characters_dir, profile_name, character_data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )
    return character_file


def load_character_file(characters_dir, profile_name):
    character_file = characters_dir / f"{profile_name}.json"
    return json.loads(character_file.read_text(encoding="utf-8"))


def make_trait_dictionary():
    return [
        {
            "regeneration": {
                "desc": "Gain +2 Regeneration at level 1 and an additional +1 at 5, 10, 15, and 20",
                "bonus": [2, 3, 4, 5, 6],
            },
            "brawler": {
                "desc": "Gain +1 to hit at level 1, 5, 10, 15, and 20",
                "bonus": [1, 2, 3, 4, 5],
            },
            "thug": {
                "desc": "Gain +1 to damage at level 1, 5, 10, 15, and 20",
                "bonus": [1, 2, 3, 4, 5],
            },
            "hearty": {
                "desc": "Gain +6 Hit Points at level 1, 5, 10, 15, and 20",
                "bonus": [6, 12, 18, 24, 30],
            },
            "nimble": {
                "desc": "Gain +1 Armor Class at level 1, 5, 10, 15, and 20",
                "bonus": [1, 2, 3, 4, 5],
            },
            "thickskinned": {
                "desc": "Gain +2 DR at level 1, and +1 additional at 5, 10, 15, and 20",
                "bonus": [2, 3, 4, 5, 6],
            },
            "opportunist": {
                "desc": "Gain +2 to initiative at level 1, and +1 additional at 5, 10, 15, and 20",
                "bonus": [2, 3, 4, 5, 6],
            },
            "nebulous": {
                "desc": "Gain +6% to blur at level 1, and +1% additional at 5, 10, 15, and 20",
                "bonus": [6, 7, 8, 9, 10],
            },
            "cursed": {
                "desc": "Take a penalty on hit, damage, and armor class.",
                "bonus": [5, 8, 11, 15, 18],
            },
        }
    ]


def make_base_character(trait="", traitregen=0, traithp=0, regeneration=0):
    return {
        "name": "Test Hero",
        "level": 1,
        "build": "strength",
        "trait": trait,
        "hp": 30,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 2,
        "damage": 2,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 1000,
        "strength": 6,
        "dexterity": 4,
        "constitution": 4,
        "remaining feats": 0,
        "ap": 15,
        "apboost": False,
        "regeneration": regeneration,
        "feats taken": [],
        "armor": {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a"},
        "equip": "",
        "hfeats taken": [],
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "forfeits": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "thp": 1,
        "tac": 1,
        "thit": 1,
        "tdamage": 1,
        "tdr": 1,
        "dexfighter": 0,
        "renown": 0,
        "initiative": 1,
        "potions": [],
        "potioneffect": "",
        "potionhit": 0,
        "potiondamage": 0,
        "potionac": 0,
        "potionhp": 0,
        "potionblur": 0,
        "potionstr": 0,
        "potiondex": 0,
        "potioncon": 0,
        "potionregen": 0,
        "pstrength": 0,
        "pdexterity": 0,
        "pconstitution": 0,
        "armorhit": 0,
        "armordamage": 0,
        "armorac": 0,
        "armorhp": 0,
        "armordr": 0,
        "armorstrength": 0,
        "armordexterity": 0,
        "armorconstitution": 0,
        "armorblur": 0,
        "armorinitiative": 0,
        "blur": 0,
        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traitdr": 0,
        "traithp": traithp,
        "traitregen": traitregen,
        "cursed": 0,
        "status": "",
        "statuscounter": 0,
        "fight": 0,
    }


def test_pri_6_trait_refreshes_saved_combat_totals_after_successful_trait_selection(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(),
    )

    trait_dictionary = make_trait_dictionary()
    trait_list = list(trait_dictionary[0].keys())

    result = pri_6_trait(
        character="test profile",
        message="!traitpick hearty",
        traitList=trait_list,
        traitDictionary=trait_dictionary,
        trait="hearty",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == "The trait 'Hearty' has been added to your character sheet."
    assert saved_character["trait"] == "hearty"
    assert saved_character["traithp"] == 6
    assert saved_character["thp"] == 46
    assert saved_character["tac"] == 14
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 6
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_6_trait_invalid_trait_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(regeneration=99),
    )

    trait_dictionary = make_trait_dictionary()
    trait_list = list(trait_dictionary[0].keys())

    result = pri_6_trait(
        character="test profile",
        message="!traitpick fake",
        traitList=trait_list,
        traitDictionary=trait_dictionary,
        trait="fake",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == "!traitpick fake is not a trait. Please use [color=pink]!traitlist[/color] for a list ot traits."
    assert saved_character["trait"] == ""
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99


def test_pri_6_trait_already_selected_trait_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(trait="hearty", traithp=6, regeneration=99),
    )

    trait_dictionary = make_trait_dictionary()
    trait_list = list(trait_dictionary[0].keys())

    result = pri_6_trait(
        character="test profile",
        message="!traitpick brawler",
        traitList=trait_list,
        traitDictionary=trait_dictionary,
        trait="brawler",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == "You've already selected a trait. If you wish to change it, you must !respec if you have the points."
    assert saved_character["trait"] == "hearty"
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99
