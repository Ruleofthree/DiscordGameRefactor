import json

from src.character_repository import create_character


def write_levelchart(char_folder):
    levelchart = {
        "1": [
            30,   # hp
            1,    # number of dice
            10,   # number of sides
            15,   # ap
            2,    # total feats
            0,    # hit and damage
            10,   # ac
            100   # next level xp
        ]
    }

    (char_folder / "levelchart.json").write_text(
        json.dumps(levelchart),
        encoding="utf-8",
    )


def write_player_database(char_folder, data=None):
    if data is None:
        data = {}

    (char_folder / "playerDatabase.json").write_text(
        json.dumps(data),
        encoding="utf-8",
    )


def test_create_character_creates_character_sheet_and_updates_player_database(tmp_path):
    char_folder = tmp_path
    write_levelchart(char_folder)
    write_player_database(char_folder)

    create_character(
        character="Their Perfect Doll",
        name="Kysume",
        char_folder=char_folder,
    )

    character_file = char_folder / "their perfect doll.json"
    assert character_file.is_file()

    character_data = json.loads(character_file.read_text(encoding="utf-8"))

    assert character_data["name"] == "Kysume"
    assert character_data["level"] == 1
    assert character_data["build"] == ""
    assert character_data["trait"] == ""
    assert character_data["hp"] == 30
    assert character_data["total feats"] == 2
    assert character_data["base damage"] == "1d10"
    assert character_data["hit"] == 0
    assert character_data["damage"] == 0
    assert character_data["ac"] == 10
    assert character_data["currentxp"] == 0
    assert character_data["nextlevel"] == 100
    assert character_data["remaining feats"] == 2
    assert character_data["ap"] == 15
    assert character_data["feats taken"] == []
    assert character_data["hfeats taken"] == []
    assert character_data["potions"] == []
    assert character_data["armor"] == {
        "armor1": "n/a",
        "armor2": "n/a",
        "armor3": "n/a",
    }
    assert character_data["wins"] == 0
    assert character_data["losses"] == 0
    assert character_data["forfeits"] == 0
    assert character_data["renown"] == 0
    assert character_data["fight"] == 0
    assert character_data["status"] == ""

    player_database = json.loads(
        (char_folder / "playerDatabase.json").read_text(encoding="utf-8")
    )

    assert player_database == {
        "Kysume": "their perfect doll",
    }


def test_create_character_does_not_overwrite_existing_character(tmp_path):
    char_folder = tmp_path
    write_levelchart(char_folder)
    write_player_database(char_folder, {"Existing Name": "their perfect doll"})

    existing_file = char_folder / "their perfect doll.json"
    existing_data = {
        "name": "Existing Name",
        "level": 99,
    }
    existing_file.write_text(json.dumps(existing_data), encoding="utf-8")

    result = create_character(
        character="Their Perfect Doll",
        name="Kysume",
        char_folder=char_folder,
    )

    character_data = json.loads(existing_file.read_text(encoding="utf-8"))
    player_database = json.loads(
        (char_folder / "playerDatabase.json").read_text(encoding="utf-8")
    )

    assert result is False
    assert character_data == existing_data
    assert player_database == {
        "Existing Name": "their perfect doll",
    }