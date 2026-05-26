import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onPRIUtils import pri_11_givepotion


def write_character(characters_dir, profile_name, data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )
    return character_file


def read_character(characters_dir, profile_name):
    return json.loads(
        (characters_dir / f"{profile_name}.json").read_text(encoding="utf-8")
    )


def test_pri_11_givepotion_transfers_potion_between_character_files(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "alice",
        {
            "name": "alice",
            "potions": ["hp5", "hit1"],
        },
    )
    write_character(
        characters_dir,
        "bob",
        {
            "name": "bob",
            "potions": ["damage1"],
        },
    )

    msg, gifter, gifted = pri_11_givepotion(
        "alice",
        "hp5",
        "bob",
        str(characters_dir) + "/",
    )

    assert msg == "alice has given bob a potion of hp5"
    assert gifter == "alice"
    assert gifted == "bob"

    assert read_character(characters_dir, "alice")["potions"] == ["hit1"]
    assert read_character(characters_dir, "bob")["potions"] == ["damage1", "hp5"]


def test_pri_11_givepotion_does_not_transfer_missing_potion(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "alice",
        {
            "name": "alice",
            "potions": ["hit1"],
        },
    )
    write_character(
        characters_dir,
        "bob",
        {
            "name": "bob",
            "potions": ["damage1"],
        },
    )

    msg, gifter, gifted = pri_11_givepotion(
        "alice",
        "hp5",
        "bob",
        str(characters_dir) + "/",
    )

    assert msg == "You do not have this item to give."
    assert gifter == "alice"
    assert gifted == "bob"

    assert read_character(characters_dir, "alice")["potions"] == ["hit1"]
    assert read_character(characters_dir, "bob")["potions"] == ["damage1"]


def test_pri_11_givepotion_does_not_transfer_when_recipient_inventory_full(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "alice",
        {
            "name": "alice",
            "potions": ["hp5", "hit1"],
        },
    )
    write_character(
        characters_dir,
        "bob",
        {
            "name": "bob",
            "potions": ["damage1", "damage2", "ac1", "tstr1"],
        },
    )

    msg, gifter, gifted = pri_11_givepotion(
        "alice",
        "hp5",
        "bob",
        str(characters_dir) + "/",
    )

    assert (
        msg
        == "You can not give bob anything, as they have no space in their inventory to take this item."
    )
    assert gifter == "alice"
    assert gifted == "bob"

    assert read_character(characters_dir, "alice")["potions"] == ["hp5", "hit1"]
    assert read_character(characters_dir, "bob")["potions"] == [
        "damage1",
        "damage2",
        "ac1",
        "tstr1",
    ]


def test_pri_11_givepotion_returns_message_when_sender_file_missing(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "bob",
        {
            "name": "bob",
            "potions": [],
        },
    )

    msg = pri_11_givepotion(
        "alice",
        "hp5",
        "bob",
        str(characters_dir) + "/",
    )

    assert msg == "You do not have a character to use this command."


def test_pri_11_givepotion_returns_message_when_recipient_file_missing(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_character(
        characters_dir,
        "alice",
        {
            "name": "alice",
            "potions": ["hp5"],
        },
    )

    msg = pri_11_givepotion(
        "alice",
        "hp5",
        "bob",
        str(characters_dir) + "/",
    )

    assert msg == "You can not give this posiont, as bob does not have a character."
    assert read_character(characters_dir, "alice")["potions"] == ["hp5"]