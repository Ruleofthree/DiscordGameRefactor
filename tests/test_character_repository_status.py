import json

from src.character_repository import (apply_passive_status_timer_tick,
                                      update_character_status_from_status_message,
                                      )


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


def write_timer_character(
    characters_dir,
    profile_name,
    status="",
    statuscounter=0,
    renown=0,
):
    character_data = {
        "name": profile_name.title(),
        "status": status,
        "statuscounter": statuscounter,
        "renown": renown,
    }
    character_file = characters_dir / f"{profile_name}.json"
    character_file.write_text(json.dumps(character_data), encoding="utf-8")
    return character_file


def test_apply_passive_status_timer_tick_grants_renown_in_ooc_room(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_timer_character(
        characters_dir,
        "alice",
        status=ROOM_ID,
        statuscounter=0,
        renown=100,
    )

    new_counter, updated_profiles = apply_passive_status_timer_tick(
        ["alice"],
        counter=0,
        characters_dir=characters_dir,
    )

    saved_character = read_character(characters_dir, "alice")

    assert saved_character["renown"] == 110
    assert saved_character["statuscounter"] == 1
    assert new_counter == 1
    assert updated_profiles == ["alice"]


def test_apply_passive_status_timer_tick_does_not_grant_renown_outside_ooc_room(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_timer_character(
        characters_dir,
        "alice",
        status="adh-other-room",
        statuscounter=0,
        renown=100,
    )

    new_counter, updated_profiles = apply_passive_status_timer_tick(
        ["alice"],
        counter=0,
        characters_dir=characters_dir,
    )

    saved_character = read_character(characters_dir, "alice")

    assert saved_character["renown"] == 100
    assert saved_character["statuscounter"] == 0
    assert new_counter == 1
    assert updated_profiles == []


def test_apply_passive_status_timer_tick_does_not_grant_renown_after_statuscounter_cap(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_timer_character(
        characters_dir,
        "alice",
        status=ROOM_ID,
        statuscounter=11,
        renown=100,
    )

    new_counter, updated_profiles = apply_passive_status_timer_tick(
        ["alice"],
        counter=0,
        characters_dir=characters_dir,
    )

    saved_character = read_character(characters_dir, "alice")

    assert saved_character["renown"] == 100
    assert saved_character["statuscounter"] == 11
    assert new_counter == 1
    assert updated_profiles == []


def test_apply_passive_status_timer_tick_resets_statuscounter_when_counter_is_24(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    write_timer_character(
        characters_dir,
        "alice",
        status=ROOM_ID,
        statuscounter=7,
        renown=100,
    )

    new_counter, updated_profiles = apply_passive_status_timer_tick(
        ["alice"],
        counter=24,
        characters_dir=characters_dir,
    )

    saved_character = read_character(characters_dir, "alice")

    assert saved_character["renown"] == 100
    assert saved_character["statuscounter"] == 0
    assert new_counter == 25
    assert updated_profiles == []


def test_apply_passive_status_timer_tick_wraps_counter_after_25(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    new_counter, updated_profiles = apply_passive_status_timer_tick(
        [],
        counter=25,
        characters_dir=characters_dir,
    )

    assert new_counter == 0
    assert updated_profiles == []


def test_apply_passive_status_timer_tick_skips_missing_character_files(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    new_counter, updated_profiles = apply_passive_status_timer_tick(
        ["missing"],
        counter=0,
        characters_dir=characters_dir,
    )

    assert new_counter == 1
    assert updated_profiles == []