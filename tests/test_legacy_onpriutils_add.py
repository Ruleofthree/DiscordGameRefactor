import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_4_add


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


def make_base_character(apboost=True):
    return {
        "name": "Test Hero",
        "strength": 1,
        "dexterity": 2,
        "constitution": 3,
        "apboost": apboost,
    }


def test_pri_4_add_adds_strength_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add strength",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 2
    assert saved_character["dexterity"] == 2
    assert saved_character["constitution"] == 3
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_strength_abbreviation_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add str",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 2
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_dexterity_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add dexterity",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 1
    assert saved_character["dexterity"] == 3
    assert saved_character["constitution"] == 3
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_dexterity_abbreviation_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add dex",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["dexterity"] == 3
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_constitution_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add constitution",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 1
    assert saved_character["dexterity"] == 2
    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_adds_constitution_abbreviation_when_apboost_is_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add con",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["constitution"] == 4
    assert saved_character["apboost"] is False
    assert result == [
        "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] to ensure changes."
    ]


def test_pri_4_add_rejects_invalid_ability(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=True),
    )

    result = pri_4_add(
        message="!add wisdom",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 1
    assert saved_character["dexterity"] == 2
    assert saved_character["constitution"] == 3
    assert saved_character["apboost"] is True
    assert result == [
        "You need to specify the ability you want to point the point to. Type '!add str' or '!add strength' for strength, and so on."
    ]


def test_pri_4_add_rejects_when_apboost_is_not_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(apboost=False),
    )

    result = pri_4_add(
        message="!add strength",
        character="test profile",
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["strength"] == 1
    assert saved_character["dexterity"] == 2
    assert saved_character["constitution"] == 3
    assert saved_character["apboost"] is False
    assert result == [
        "You do not have any more ability points to spend."
    ]