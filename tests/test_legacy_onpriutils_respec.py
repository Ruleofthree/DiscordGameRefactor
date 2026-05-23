import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_7_respec


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


def make_respec_character(reset=3, renown=500):
    return {
        "name": "Test Hero",
        "level": 5,
        "build": "strength",
        "base damage": "2d6",
        "strength": 6,
        "dexterity": 4,
        "constitution": 5,
        "regeneration": 2,
        "traithit": 1,
        "traitdamage": 1,
        "traitac": 1,
        "traitdr": 1,
        "traithp": 5,
        "traitregen": 1,
        "cursed": 0,
        "initiative": 2,
        "blur": 1,
        "feats taken": ["focus", "power attack"],
        "hfeats taken": ["focus", "power attack"],
        "feathp": 5,
        "feathit": 1,
        "featdamage": 1,
        "featac": 1,
        "dexfighter": 1,
        "remaining feats": 0,
        "reset": reset,
        "tdr": 1,
        "trait": "brawler",
        "total feats": 2,
        "renown": renown,
    }


def assert_character_was_reset(saved_character, expected_reset):
    assert saved_character["build"] == ""
    assert saved_character["base damage"] == "1d10"
    assert saved_character["strength"] == 0
    assert saved_character["dexterity"] == 0
    assert saved_character["constitution"] == 0
    assert saved_character["regeneration"] == 0
    assert saved_character["traithit"] == 0
    assert saved_character["traitdamage"] == 0
    assert saved_character["traitac"] == 0
    assert saved_character["traitdr"] == 0
    assert saved_character["traithp"] == 0
    assert saved_character["traitregen"] == 0
    assert saved_character["cursed"] == 0
    assert saved_character["initiative"] == 0
    assert saved_character["blur"] == 0
    assert saved_character["feats taken"] == []
    assert saved_character["hfeats taken"] == []
    assert saved_character["feathp"] == 0
    assert saved_character["feathit"] == 0
    assert saved_character["featdamage"] == 0
    assert saved_character["featac"] == 0
    assert saved_character["dexfighter"] == 0
    assert saved_character["remaining feats"] == 2
    assert saved_character["reset"] == expected_reset
    assert saved_character["tdr"] == 0
    assert saved_character["trait"] == ""


def test_pri_7_respec_uses_reset_point_when_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_respec_character(reset=3, renown=500),
    )

    result = pri_7_respec("test profile")

    saved_character = load_character_file(characters_dir, "test profile")

    assert_character_was_reset(saved_character, expected_reset=2)
    assert saved_character["renown"] == 500
    assert "your characters abilities, trait, and feats have been reset" in result
    assert "you have [color=red]2[/color] reset points remaining" in result


def test_pri_7_respec_uses_renown_when_no_reset_points_are_available(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_respec_character(reset=0, renown=500),
    )

    result = pri_7_respec("test profile")

    saved_character = load_character_file(characters_dir, "test profile")

    assert_character_was_reset(saved_character, expected_reset=0)

    # This locks current legacy behavior. The function calculates renown -= 250,
    # but does not currently write that new renown value back to charData.
    assert saved_character["renown"] == 500

    assert "your characters abilities, trait, and feats have been reset" in result
    assert "As you had no reset points, [color=yellow]250 renown[/color] was taken from your total" in result


def test_pri_7_respec_rejects_when_no_reset_points_or_enough_renown(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    original_character = make_respec_character(reset=0, renown=250)

    make_character_file(
        characters_dir,
        "test profile",
        original_character,
    )

    result = pri_7_respec("test profile")

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character == original_character
    assert result == "You currently have no more reset points to use, or renown to spend."


def test_pri_7_respec_rejects_when_renown_is_below_required_amount(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    original_character = make_respec_character(reset=0, renown=249)

    make_character_file(
        characters_dir,
        "test profile",
        original_character,
    )

    result = pri_7_respec("test profile")

    saved_character = load_character_file(characters_dir, "test profile")

    assert saved_character == original_character
    assert result == "You currently have no more reset points to use, or renown to spend."