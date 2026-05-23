import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onMSGUtils import status_compile


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


def make_base_character(status="", statuscounter=0):
    return {
        "name": "Test Hero",
        "status": status,
        "statuscounter": statuscounter,
        "renown": 0,
    }


def test_status_compile_sets_status_when_character_is_in_master_list_and_room_is_found(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(status=""),
    )

    status_message = (
        "Online [session=Unspoiled Desire (Command and OoC Room)]"
        "adh-8216a753c1ef08445052[/session]"
    )

    status_compile(
        character="test profile",
        statusmsg=status_message,
        masterList=["test profile"],
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["status"] == "adh-8216a753c1ef08445052"
    assert saved_character["statuscounter"] == 0
    assert saved_character["renown"] == 0


def test_status_compile_leaves_status_unchanged_when_room_is_not_found(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(status="adh-8216a753c1ef08445052"),
    )

    status_message = (
        "Online [session=Some Other Room]"
        "adh-not-the-target-room[/session]"
    )

    status_compile(
        character="test profile",
        statusmsg=status_message,
        masterList=["test profile"],
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["status"] == "adh-8216a753c1ef08445052"


def test_status_compile_does_nothing_when_character_is_not_in_master_list(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(status="existing-status"),
    )

    status_message = (
        "Online [session=Unspoiled Desire (Command and OoC Room)]"
        "adh-8216a753c1ef08445052[/session]"
    )

    status_compile(
        character="test profile",
        statusmsg=status_message,
        masterList=["other profile"],
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["status"] == "existing-status"


def test_status_compile_swallows_missing_character_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    status_message = (
        "Online [session=Unspoiled Desire (Command and OoC Room)]"
        "adh-8216a753c1ef08445052[/session]"
    )

    result = status_compile(
        character="missing profile",
        statusmsg=status_message,
        masterList=["missing profile"],
    )

    assert result is None


def test_status_compile_swallows_malformed_status_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(status="existing-status"),
    )

    status_compile(
        character="test profile",
        statusmsg="Malformed status message without expected session marker",
        masterList=["test profile"],
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character["status"] == "existing-status"