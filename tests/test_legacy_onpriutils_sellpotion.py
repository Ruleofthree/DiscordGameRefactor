import pytest
import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_11_sellpotion


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


def make_potion_seller(potions=None, renown=100):
    if potions is None:
        potions = []

    return {
        "name": "Test Hero",
        "renown": renown,
        "potions": potions,
    }


def test_pri_11_sellpotion_sells_owned_potion_and_adds_half_value(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_potion_seller(potions=["hp5"], renown=100),
    )

    result = pri_11_sellpotion("tester", "hp5", str(characters_dir) + "/")

    assert result == "Test Hero has sold a [color=red]hp5[/color] for [color=yellow]75 renown[/color]."

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 175
    assert saved_character["potions"] == []


def test_pri_11_sellpotion_rejects_missing_potion_without_changing_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_potion_seller(potions=["hp5"], renown=100),
    )

    result = pri_11_sellpotion("tester", "damage1", str(characters_dir) + "/")

    assert result == "You do not have that potion to sell."

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 100
    assert saved_character["potions"] == ["hp5"]


def test_pri_11_sellpotion_handles_unknown_potion_data_without_changing_character(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()
    make_character_file(
        characters_dir,
        "tester",
        make_potion_seller(potions=["fake potion"], renown=100),
    )

    result = pri_11_sellpotion("tester", "fake potion", str(characters_dir) + "/")

    assert result == "That potion does not exist in the potion data."

    saved_character = load_character_file(characters_dir, "tester")
    assert saved_character["renown"] == 100
    assert saved_character["potions"] == ["fake potion"]


def test_pri_11_sellpotion_missing_character_preserves_legacy_unbound_local_error(tmp_path):
    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    with pytest.raises(UnboundLocalError):
        pri_11_sellpotion("missing", "hp5", str(characters_dir) + "/")