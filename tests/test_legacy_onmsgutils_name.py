import json
from pathlib import Path

from original.onMSGUtils import message_5_name


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


def test_message_5_name_requires_character_name(tmp_path):
    char_folder = tmp_path
    char_file = char_folder / "their perfect doll.json"

    result = message_5_name(
        channel="test-channel",
        charFolder=char_folder,
        message="!name",
        charFile=char_file,
        character="Their Perfect Doll",
    )

    assert result == ["You need to give your character a name."]


def test_message_5_name_rejects_existing_character(tmp_path):
    char_folder = tmp_path
    char_file = char_folder / "their perfect doll.json"

    char_file.write_text(
        json.dumps({"name": "Existing Character"}),
        encoding="utf-8",
    )

    result = message_5_name(
        channel="test-channel",
        charFolder=char_folder,
        message="!name Kysume",
        charFile=char_file,
        character="Their Perfect Doll",
    )

    assert result == ["You've already created a character."]


def test_message_5_name_creates_character_and_returns_legacy_messages(tmp_path):
    char_folder = tmp_path
    char_file = char_folder / "their perfect doll.json"

    write_levelchart(char_folder)
    write_player_database(char_folder)

    result = message_5_name(
        channel="test-channel",
        charFolder=char_folder,
        message="!name Kysume",
        charFile=char_file,
        character="Their Perfect Doll",
    )

    assert result == [
        "Your character name is: Kysume",
        "Your character sheet has been created.",
        "PM [color=pink]Unspoiled Desire[/color] with '!build <strength> <constitution> <dexterity>' to"
        " determine general build path, and bonuses obtained from selected feats. Example: !build strength",
    ]

    assert char_file.is_file()

    character_data = json.loads(char_file.read_text(encoding="utf-8"))
    assert character_data["name"] == "Kysume"
    assert character_data["level"] == 1
    assert character_data["base damage"] == "1d10"

    player_database = json.loads(
        (char_folder / "playerDatabase.json").read_text(encoding="utf-8")
    )

    assert player_database == {
        "Kysume": "their perfect doll",
    }