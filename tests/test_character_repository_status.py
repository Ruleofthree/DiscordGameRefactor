import json

from src.character_repository import update_character_status_from_status_message


ROOM_ID = "adh-8216a753c1ef08445052"


def write_character(characters_dir, profile_name, status="old-status"):
    character_data = {
        "name": profile_name.title(),
        "status": status,
    }
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(json.dumps(character_data), encoding="utf-8")
    return character_file


def read_character(characters_dir, profile_name):
    return json.loads((characters_dir / f"{profile_name}.json").read_text(encoding="utf-8"))


def test_update_character_status_sets_ooc_room_for_exact_legacy_status_message(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "alice")

    statusmsg = "[session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]"

    update_character_status_from_status_message(
        "alice",
        statusmsg,
        ["alice"],
        characters_dir,
    )

    assert read_character(characters_dir, "alice")["status"] == ROOM_ID


def test_update_character_status_does_nothing_when_character_not_in_master_list(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "alice", status="old-status")

    statusmsg = "[session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]"

    update_character_status_from_status_message(
        "alice",
        statusmsg,
        [],
        characters_dir,
    )

    assert read_character(characters_dir, "alice")["status"] == "old-status"


def test_update_character_status_preserves_broad_exception_behavior_for_malformed_status(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    write_character(characters_dir, "alice", status="old-status")

    update_character_status_from_status_message(
        "alice",
        "malformed status text",
        ["alice"],
        characters_dir,
    )

    assert read_character(characters_dir, "alice")["status"] == "old-status"