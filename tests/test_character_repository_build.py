import json

from src.character_repository import select_character_build


def write_character(tmp_path, character_name="testplayer", character_data=None):
    if character_data is None:
        character_data = {
            "name": "Test Character",
            "level": 1,
            "build": "",
            "feats taken": [],
        }

    character_path = tmp_path / f"{character_name}.json"
    character_path.write_text(
        json.dumps(character_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return character_path


def read_character(character_path):
    return json.loads(character_path.read_text(encoding="utf-8"))


def test_select_character_build_sets_strength_build(tmp_path):
    character_path = write_character(tmp_path)

    msg = select_character_build("testplayer", "strength", tmp_path)

    character_data = read_character(character_path)

    assert character_data["build"] == "strength"
    assert msg == (
        "You have identified your character as a strength build, and it has been recorded as such in your character sheet. "
        "Please ues [color=pink]!stats[/color] command to select your stat points, before selecting feats."
    )


def test_select_character_build_adds_focus_for_low_level_strength_build(tmp_path):
    character_path = write_character(
        tmp_path,
        character_data={
            "name": "Test Character",
            "level": 3,
            "build": "",
            "feats taken": [],
        },
    )

    select_character_build("testplayer", "strength", tmp_path)

    character_data = read_character(character_path)

    assert character_data["feats taken"] == ["focus"]


def test_select_character_build_does_not_add_focus_for_higher_level_strength_build(tmp_path):
    character_path = write_character(
        tmp_path,
        character_data={
            "name": "Test Character",
            "level": 4,
            "build": "",
            "feats taken": [],
        },
    )

    select_character_build("testplayer", "strength", tmp_path)

    character_data = read_character(character_path)

    assert character_data["build"] == "strength"
    assert character_data["feats taken"] == []


def test_select_character_build_sets_dexterity_build_without_focus(tmp_path):
    character_path = write_character(tmp_path)

    select_character_build("testplayer", "dexterity", tmp_path)

    character_data = read_character(character_path)

    assert character_data["build"] == "dexterity"
    assert character_data["feats taken"] == []


def test_select_character_build_sets_constitution_build_without_focus(tmp_path):
    character_path = write_character(tmp_path)

    select_character_build("testplayer", "constitution", tmp_path)

    character_data = read_character(character_path)

    assert character_data["build"] == "constitution"
    assert character_data["feats taken"] == []


def test_select_character_build_does_not_overwrite_existing_build(tmp_path):
    character_path = write_character(
        tmp_path,
        character_data={
            "name": "Test Character",
            "level": 1,
            "build": "dexterity",
            "feats taken": [],
        },
    )

    msg = select_character_build("testplayer", "strength", tmp_path)

    character_data = read_character(character_path)

    assert character_data["build"] == "dexterity"
    assert character_data["feats taken"] == []
    assert msg == "You already have selected a build."


def test_select_character_build_preserves_existing_character_fields(tmp_path):
    character_path = write_character(
        tmp_path,
        character_data={
            "name": "Test Character",
            "level": 1,
            "build": "",
            "feats taken": [],
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "renown": 125,
        },
    )

    select_character_build("testplayer", "constitution", tmp_path)

    character_data = read_character(character_path)

    assert character_data["name"] == "Test Character"
    assert character_data["level"] == 1
    assert character_data["strength"] == 0
    assert character_data["dexterity"] == 0
    assert character_data["constitution"] == 0
    assert character_data["renown"] == 125