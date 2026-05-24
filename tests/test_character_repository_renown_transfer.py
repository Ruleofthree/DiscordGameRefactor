import json

import pytest

from src.character_repository import transfer_character_renown


def write_character(characters_dir, profile_name, data):
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )
    return character_file


def load_character_file(characters_dir, profile_name):
    character_file = characters_dir / f"{profile_name}.json"
    return json.loads(character_file.read_text(encoding="utf-8"))


def base_character(name, renown):
    return {
        "name": name,
        "renown": renown,
    }


def test_transfer_character_renown_successfully_moves_renown_between_characters(tmp_path):
    write_character(tmp_path, "giver", base_character("Giver Name", 100))
    write_character(tmp_path, "receiver", base_character("Receiver Name", 25))

    msg = transfer_character_renown(
        "giver",
        "receiver",
        40,
        tmp_path,
    )

    assert msg == "Giver Name has given Receiver Name[color=yellow] 40[/color] renown"

    giver_data = load_character_file(tmp_path, "giver")
    receiver_data = load_character_file(tmp_path, "receiver")

    assert giver_data["renown"] == 60
    assert receiver_data["renown"] == 65


def test_transfer_character_renown_returns_legacy_message_when_gifter_is_missing(tmp_path):
    write_character(tmp_path, "receiver", base_character("Receiver Name", 25))

    msg = transfer_character_renown(
        "missing",
        "receiver",
        40,
        tmp_path,
    )

    assert msg == "missing does not have a character to use this command."

    receiver_data = load_character_file(tmp_path, "receiver")
    assert receiver_data["renown"] == 25


def test_transfer_character_renown_returns_legacy_message_when_recipient_is_missing(tmp_path):
    write_character(tmp_path, "giver", base_character("Giver Name", 100))

    msg = transfer_character_renown(
        "giver",
        "missing",
        40,
        tmp_path,
    )

    assert msg == "missing does not have a character to use this command."

    giver_data = load_character_file(tmp_path, "giver")
    assert giver_data["renown"] == 100


def test_transfer_character_renown_rejects_transfer_when_gifter_has_insufficient_renown(tmp_path):
    write_character(tmp_path, "giver", base_character("Giver Name", 30))
    write_character(tmp_path, "receiver", base_character("Receiver Name", 25))

    msg = transfer_character_renown(
        "giver",
        "receiver",
        40,
        tmp_path,
    )

    assert msg == "You do not have this much to give."

    giver_data = load_character_file(tmp_path, "giver")
    receiver_data = load_character_file(tmp_path, "receiver")

    assert giver_data["renown"] == 30
    assert receiver_data["renown"] == 25