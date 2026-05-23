import json

from src.character_repository import select_character_trait


def write_character(tmp_path, profile_name="tester", **overrides):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    character = {
        "name": "Test Character",
        "level": 1,
        "trait": "",
        "traitregen": 0,
        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traitdr": 0,
        "traithp": 0,
        "initiative": 0,
        "blur": 0,
        "cursed": 0,
        "strength": 5,
        "dexterity": 5,
        "constitution": 5,
        "tdr": 0,
        "regeneration": 0,
    }
    character.update(overrides)

    character_file = char_folder / f"{profile_name}.json"
    character_file.write_text(json.dumps(character), encoding="utf-8")

    return char_folder, character_file


def trait_dictionary():
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
                "desc": "Take a penalty",
                "bonus": [5, 8, 11, 15, 18],
            },
        }
    ]


def trait_list():
    return list(trait_dictionary()[0].keys())


def read_character(character_file):
    return json.loads(character_file.read_text(encoding="utf-8"))


def test_select_character_trait_adds_regeneration_at_level_one(tmp_path):
    char_folder, character_file = write_character(tmp_path)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick regeneration",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="regeneration",
    )

    character = read_character(character_file)

    assert msg == "The trait Regeneration' has been added to your character sheet."
    assert character["trait"] == "regeneration"
    assert character["traitregen"] == 2


def test_select_character_trait_adds_brawler_at_level_five(tmp_path):
    char_folder, character_file = write_character(tmp_path, level=5)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick brawler",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="brawler",
    )

    character = read_character(character_file)

    assert msg == "The trait 'Brawler' has been added to your character sheet."
    assert character["trait"] == "brawler"
    assert character["traithit"] == 2


def test_select_character_trait_adds_cursed_at_level_twenty(tmp_path):
    char_folder, character_file = write_character(tmp_path, level=20)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick cursed",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="cursed",
    )

    character = read_character(character_file)

    assert msg == "The trait 'cursed' has been added to your character sheet."
    assert character["trait"] == "cursed"
    assert character["cursed"] == 18


def test_select_character_trait_rejects_second_trait(tmp_path):
    char_folder, character_file = write_character(tmp_path, trait="thug", traitdamage=1)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick brawler",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="brawler",
    )

    character = read_character(character_file)

    assert msg == "You've already selected a trait. If you wish to change it, you must !respec if you have the points."
    assert character["trait"] == "thug"
    assert character["traitdamage"] == 1
    assert character["traithit"] == 0


def test_select_character_trait_rejects_invalid_trait_without_changing_sheet(tmp_path):
    char_folder, character_file = write_character(tmp_path)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick fake",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="fake",
    )

    character = read_character(character_file)

    assert msg == "!traitpick fake is not a trait. Please use [color=pink]!traitlist[/color] for a list ot traits."
    assert character["trait"] == ""


def test_select_character_trait_blocks_regeneration_when_tdr_is_nonzero_but_preserves_legacy_trait_write(tmp_path):
    char_folder, character_file = write_character(tmp_path, tdr=2)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick regeneration",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="regeneration",
    )

    character = read_character(character_file)

    assert msg == "You can not take regeneration as you have a non-zero value for Damage Reduction"
    assert character["trait"] == "regeneration"
    assert character["traitregen"] == 0


def test_select_character_trait_blocks_thickskinned_when_regeneration_is_nonzero_but_preserves_legacy_trait_write(tmp_path):
    char_folder, character_file = write_character(tmp_path, regeneration=2)

    msg = select_character_trait(
        char_folder=char_folder,
        character="tester",
        message="!traitpick thickskinned",
        trait_list=trait_list(),
        trait_dictionary=trait_dictionary(),
        trait="thickskinned",
    )

    character = read_character(character_file)

    assert msg == "You can not take thickskinned as you have a non-zero value for regeneration"
    assert character["trait"] == "thickskinned"
    assert character["traitdr"] == 0