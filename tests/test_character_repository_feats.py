import json

from src.character_repository import select_character_feat, load_character


def write_character(tmp_path, character_name, data):
    char_dir = tmp_path / "characters"
    char_dir.mkdir(exist_ok=True)
    path = char_dir / f"{character_name.lower()}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return char_dir


def base_character(**overrides):
    data = {
        "name": "Test Hero",
        "level": 1,
        "build": "strength",
        "hp": 20,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 1,
        "damage": 1,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 100,
        "strength": 5,
        "dexterity": 5,
        "constitution": 5,
        "remaining feats": 2,
        "feats taken": [],
        "hfeats taken": [],
        "ap": 15,
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "dexfighter": 0,
        "thp": 0,
        "tac": 0,
        "thit": 0,
        "tdamage": 0,
    }
    data.update(overrides)
    return data


def test_select_character_feat_requires_stats_first(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(strength=0, dexterity=0, constitution=0),
    )# tests/test_character_repository_feats.py

import json

from src.character_repository import load_character, select_character_feat


def write_character(tmp_path, character_name, data):
    char_dir = tmp_path / "characters"
    char_dir.mkdir(exist_ok=True)
    path = char_dir / f"{character_name.lower()}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return char_dir


def base_character(**overrides):
    data = {
        "name": "Test Hero",
        "level": 1,
        "build": "strength",
        "hp": 20,
        "total feats": 2,
        "base damage": "1d10",
        "hit": 1,
        "damage": 1,
        "ac": 10,
        "currentxp": 0,
        "nextlevel": 100,
        "strength": 5,
        "dexterity": 5,
        "constitution": 5,
        "remaining feats": 2,
        "feats taken": [],
        "hfeats taken": [],
        "ap": 15,
        "reset": 3,
        "wins": 0,
        "losses": 0,
        "abhp": 0,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "feathp": 0,
        "feathit": 0,
        "featdamage": 0,
        "featac": 0,
        "dexfigher": 0,
        "dexfighter": 0,
        "thp": 0,
        "tac": 0,
        "thit": 0,
        "tdamage": 0,
    }
    data.update(overrides)
    return data


def test_select_character_feat_requires_stats_first(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(strength=0, dexterity=0, constitution=0),
    )

    feat_dictionary = [
        {
            "power attack": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2, 3, 4, 5],
            }
        }
    ]
    feat_list = ["power attack"]

    msg = select_character_feat(
        character="tester",
        feat_name="power attack",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == [
        "Please select your character stats with the [color=pink]!stats[/color] command first."
    ]

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["feats taken"] == []
    assert saved["hfeats taken"] == []
    assert saved["remaining feats"] == 2


def test_select_character_feat_rejects_wrong_build_feat(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(build="strength"),
    )

    feat_dictionary = [
        {
            "evasion": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": "0.5",
            }
        }
    ]
    feat_list = ["evasion"]

    msg = select_character_feat(
        character="tester",
        feat_name="evasion",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == ["This feat is not available for your build choice."]

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["feats taken"] == []
    assert saved["hfeats taken"] == []
    assert saved["remaining feats"] == 2


def test_select_character_feat_rejects_second_toggle_feat(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(
            **{
                "feats taken": ["power attack"],
                "hfeats taken": ["power attack"],
            }
        ),
    )

    feat_dictionary = [
        {
            "defensive fighting": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2, 3, 4, 5],
            }
        }
    ]
    feat_list = ["defensive fighting"]

    msg = select_character_feat(
        character="tester",
        feat_name="defensive fighting",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == [
        "You can not take more than one toggle feat. You already have either [color=yellow]Power "
        "Attack[/color], [color=yellow]Defensive Fighting[/color], or [color=yellow]Masochist[/color]."
    ]


def test_select_character_feat_rejects_focus_feat(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character())

    feat_dictionary = [
        {
            "focus": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1],
            }
        }
    ]
    feat_list = ["focus"]

    msg = select_character_feat(
        character="tester",
        feat_name="focus",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == [
        "This feat is given to strength builds automatically at levels 3/9/15/18, and can not be taken "
        "in any other fashion"
    ]


def test_select_character_feat_rejects_when_no_feat_slots_remain(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(**{"remaining feats": 0}),
    )

    feat_dictionary = [
        {
            "power attack": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2, 3, 4, 5],
            }
        }
    ]
    feat_list = ["power attack"]

    msg = select_character_feat(
        character="tester",
        feat_name="power attack",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == ["You have no feat slots left to select a new feat"]


def test_select_character_feat_rejects_weaker_feat_already_hidden_taken(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(
            **{
                "feats taken": ["improved crushing blow"],
                "hfeats taken": ["crushing blow"],
            }
        ),
    )

    feat_dictionary = [
        {
            "crushing blow": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2],
            }
        }
    ]
    feat_list = ["crushing blow"]

    msg = select_character_feat(
        character="tester",
        feat_name="crushing blow",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == ["Why are you trying to take a weaker feat than the one you already have? No."]


def test_select_character_feat_rejects_unknown_feat(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character())

    feat_dictionary = [{}]
    feat_list = []

    msg = select_character_feat(
        character="tester",
        feat_name="fake feat",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == ["Make sure you have spelled the feat correctly"]

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["feats taken"] == []
    assert saved["hfeats taken"] == []
    assert saved["remaining feats"] == 2