import importlib.util
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

spec = importlib.util.spec_from_file_location(
    "legacy_onmsgutils_character_lifecycle",
    ORIGINAL_DIR / "onMSGUtils.py",
)
onMSGUtils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(onMSGUtils)


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def setup_character_folder(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_json(
        char_folder / "levelchart.json",
        {
            "1": [
                20,   # hp
                1,    # number of dice
                10,   # number of sides
                15,   # ap
                2,    # total feats
                1,    # hit and damage
                10,   # ac
                100,  # nextlevel
            ]
        },
    )

    write_json(char_folder / "playerDatabase.json", {})

    return char_folder

"""
def test_message_5_name_requires_character_name(tmp_path):
    char_folder = setup_character_folder(tmp_path)
    character = "Test Player"
    char_file = char_folder / f"{character.lower()}.json"

    msg = onMSGUtils.message_5_name(
        channel="unused",
        charFolder=str(char_folder) + "/",
        message="!name",
        charFile=char_file,
        character=character,
    )

    assert msg == ["You need to give your character a name."]
    assert not char_file.exists()
    assert read_json(char_folder / "playerDatabase.json") == {}


def test_message_5_name_refuses_existing_character(tmp_path):
    char_folder = setup_character_folder(tmp_path)
    character = "Test Player"
    char_file = char_folder / f"{character.lower()}.json"
    write_json(char_file, {"name": "Already Existing"})

    msg = onMSGUtils.message_5_name(
        channel="unused",
        charFolder=str(char_folder) + "/",
        message="!name New Name",
        charFile=char_file,
        character=character,
    )

    assert msg == ["You've already created a character."]
    assert read_json(char_file) == {"name": "Already Existing"}
    assert read_json(char_folder / "playerDatabase.json") == {}


def test_message_5_name_creates_character_sheet_and_database_entry(tmp_path):
    char_folder = setup_character_folder(tmp_path)
    character = "Test Player"
    char_file = char_folder / f"{character.lower()}.json"

    msg = onMSGUtils.message_5_name(
        channel="unused",
        charFolder=str(char_folder) + "/",
        message="!name Sir Test",
        charFile=char_file,
        character=character,
    )

    assert msg[0] == "Your character name is: Sir Test"
    assert msg[1] == "Your character sheet has been created."
    assert "PM [color=pink]Unspoiled Desire[/color]" in msg[2]

    assert char_file.exists()

    character_data = read_json(char_file)

    assert character_data["name"] == "Sir Test"
    assert character_data["level"] == 1
    assert character_data["build"] == ""
    assert character_data["trait"] == ""
    assert character_data["hp"] == 20
    assert character_data["base damage"] == "1d10"
    assert character_data["hit"] == 1
    assert character_data["damage"] == 1
    assert character_data["ac"] == 10
    assert character_data["currentxp"] == 0
    assert character_data["nextlevel"] == 100
    assert character_data["remaining feats"] == 2
    assert character_data["ap"] == 15
    assert character_data["armor"] == {
        "armor1": "n/a",
        "armor2": "n/a",
        "armor3": "n/a",
    }
    assert character_data["potions"] == []
    assert character_data["status"] == ""
    assert character_data["fight"] == 0

    player_database = read_json(char_folder / "playerDatabase.json")
    assert player_database == {"Sir Test": "test player"}
"""

def test_message_7_erase_deletes_existing_character_and_database_entry(tmp_path, monkeypatch):
    char_folder = setup_character_folder(tmp_path)
    monkeypatch.chdir(tmp_path)

    character = "Test Player"
    char_file = char_folder / f"{character.lower()}.json"

    write_json(char_file, {"name": "Sir Test"})
    write_json(char_folder / "playerDatabase.json", {"Sir Test": "test player"})

    msg = onMSGUtils.message_7_erase(character)

    assert msg == "Sir Test has been erased."
    assert not char_file.exists()
    assert read_json(char_folder / "playerDatabase.json") == {}


def test_message_7_erase_reports_missing_character(tmp_path, monkeypatch):
    char_folder = setup_character_folder(tmp_path)
    monkeypatch.chdir(tmp_path)

    character = "Missing Player"

    msg = onMSGUtils.message_7_erase(character)

    assert msg == "You don't have a character to delete."
    assert read_json(char_folder / "playerDatabase.json") == {}


def test_message_7_erase_removes_database_entry_even_if_character_file_is_missing(tmp_path, monkeypatch):
    char_folder = setup_character_folder(tmp_path)
    monkeypatch.chdir(tmp_path)

    character = "Test Player"
    write_json(char_folder / "playerDatabase.json", {"Sir Test": "test player"})

    msg = onMSGUtils.message_7_erase(character)

    assert msg == "You don't have a character to delete."
    assert read_json(char_folder / "playerDatabase.json") == {}