import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))


from onPRIUtils import pri_10_feat_pick


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


def make_base_character(**overrides):
    data = {
        "name": "Test Hero",
        "level": 1,
        "build": "strength",
        "trait": "",
        "hp": 30,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 2,
        "damage": 2,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 1000,
        "strength": 6,
        "dexterity": 4,
        "constitution": 5,
        "remaining feats": 2,
        "ap": 15,
        "apboost": False,
        "regeneration": 99,
        "feats taken": [],
        "armor": {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a"},
        "equip": "",
        "hfeats taken": [],
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "forfeits": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "thp": 1,
        "tac": 1,
        "thit": 1,
        "tdamage": 1,
        "tdr": 1,
        "dexfighter": 0,
        "renown": 0,
        "initiative": 1,
        "potions": [],
        "potioneffect": "",
        "potionhit": 0,
        "potiondamage": 0,
        "potionac": 0,
        "potionhp": 0,
        "potionblur": 0,
        "potionstr": 0,
        "potiondex": 0,
        "potioncon": 0,
        "potionregen": 0,
        "pstrength": 0,
        "pdexterity": 0,
        "pconstitution": 0,
        "armorhit": 0,
        "armordamage": 0,
        "armorac": 0,
        "armorhp": 0,
        "armordr": 0,
        "armorstrength": 0,
        "armordexterity": 0,
        "armorconstitution": 0,
        "armorblur": 0,
        "armorinitiative": 0,
        "blur": 0,
        "traithit": 0,
        "traitdamage": 0,
        "traitac": 0,
        "traitdr": 0,
        "traithp": 0,
        "traitregen": 0,
        "cursed": 0,
        "status": "",
        "statuscounter": 0,
        "fight": 0,
    }
    data.update(overrides)
    return data


def test_pri_10_feat_pick_refreshes_saved_combat_totals_after_successful_feat_selection(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(),
    )

    feat_dictionary = [
        {
            "crushing blow": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2],
            }
        }
    ]

    result = pri_10_feat_pick(
        character="test profile",
        message="!featpick crushing blow",
        featList=["crushing blow"],
        featDictionary=feat_dictionary,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == [
        "crushing blow has been added to your character sheet.",
        "Make sure you use [color=pink]!viewchar[/color] to ensure you are obtaining proper bonuses during fights.",
    ]
    assert saved_character["feats taken"] == ["crushing blow"]
    assert saved_character["hfeats taken"] == ["crushing blow"]
    assert saved_character["remaining feats"] == 1
    assert saved_character["featdamage"] == 2
    assert saved_character["thp"] == 40
    assert saved_character["tac"] == 14
    assert saved_character["tdr"] == 0
    assert saved_character["thit"] == 5
    assert saved_character["tdamage"] == 8
    assert saved_character["initiative"] == 2
    assert saved_character["regeneration"] == 0


def test_pri_10_feat_pick_invalid_feat_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(),
    )

    result = pri_10_feat_pick(
        character="test profile",
        message="!featpick fake feat",
        featList=[],
        featDictionary=[{}],
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == ["Make sure you have spelled the feat correctly"]
    assert saved_character["feats taken"] == []
    assert saved_character["hfeats taken"] == []
    assert saved_character["remaining feats"] == 2
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99


def test_pri_10_feat_pick_no_remaining_slots_does_not_refresh_stale_combat_totals(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    make_character_file(
        characters_dir,
        "test profile",
        make_base_character(**{"remaining feats": 0}),
    )

    feat_dictionary = [
        {
            "power attack": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2, 3, 4, 5],
            }
        }
    ]

    result = pri_10_feat_pick(
        character="test profile",
        message="!featpick power attack",
        featList=["power attack"],
        featDictionary=feat_dictionary,
    )

    saved_character = load_character_file(characters_dir, "test profile")

    assert result == ["You have no feat slots left to select a new feat"]
    assert saved_character["feats taken"] == []
    assert saved_character["hfeats taken"] == []
    assert saved_character["remaining feats"] == 0
    assert saved_character["thp"] == 1
    assert saved_character["tac"] == 1
    assert saved_character["tdr"] == 1
    assert saved_character["thit"] == 1
    assert saved_character["tdamage"] == 1
    assert saved_character["initiative"] == 1
    assert saved_character["regeneration"] == 99
