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


def test_select_character_feat_adds_valid_feat_to_visible_and_hidden_lists(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character())

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
        "power attack has been added to your character sheet.",
        "Make sure you use [color=pink]!viewchar[/color] to ensure you are obtaining proper bonuses during fights.",
    ]

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["feats taken"] == ["power attack"]
    assert saved["hfeats taken"] == ["power attack"]
    assert saved["remaining feats"] == 1


def test_select_character_feat_rejects_when_level_too_low(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character(level=1))

    feat_dictionary = [
        {
            "titan blow": {
                "requirements": [18, 0, 0, 0, "greater crushing blow"],
                "action": [10, 14],
            }
        }
    ]
    feat_list = ["titan blow"]

    msg = select_character_feat(
        character="tester",
        feat_name="titan blow",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == ["You are not the required level for this feat."]


def test_select_character_feat_rejects_missing_prerequisite_feat(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character(level=6))

    feat_dictionary = [
        {
            "improved crushing blow": {
                "requirements": [6, 0, 0, 0, "crushing blow"],
                "action": [3, 5],
            }
        }
    ]
    feat_list = ["improved crushing blow"]

    msg = select_character_feat(
        character="tester",
        feat_name="improved crushing blow",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    assert msg == ["You do hot have the required prerequisites to take this feat."]

def test_select_character_feat_crushing_blow_adds_featdamage(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character())

    feat_dictionary = [
        {
            "crushing blow": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1, 2],
            }
        }
    ]
    feat_list = ["crushing blow"]

    select_character_feat(
        character="tester",
        feat_name="crushing blow",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["featdamage"] == 2
    assert saved["feats taken"] == ["crushing blow"]
    assert saved["hfeats taken"] == ["crushing blow"]
    assert saved["remaining feats"] == 1


def test_select_character_feat_improved_crushing_blow_replaces_visible_lower_feat(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(
            level=6,
            **{
                "remaining feats": 1,
                "feats taken": ["crushing blow"],
                "hfeats taken": ["crushing blow"],
                "featdamage": 2,
            },
        ),
    )

    feat_dictionary = [
        {
            "improved crushing blow": {
                "requirements": [6, 0, 0, 0, "crushing blow"],
                "action": [3, 5],
            }
        }
    ]
    feat_list = ["improved crushing blow"]

    select_character_feat(
        character="tester",
        feat_name="improved crushing blow",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["featdamage"] == 4
    assert saved["feats taken"] == ["improved crushing blow"]
    assert saved["hfeats taken"] == ["crushing blow", "improved crushing blow"]
    assert saved["remaining feats"] == 0


def test_select_character_feat_precision_strike_adds_feathit(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character())

    feat_dictionary = [
        {
            "precision strike": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": 1,
            }
        }
    ]
    feat_list = ["precision strike"]

    select_character_feat(
        character="tester",
        feat_name="precision strike",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["feathit"] == 2
    assert saved["feats taken"] == ["precision strike"]
    assert saved["hfeats taken"] == ["precision strike"]


def test_select_character_feat_lightning_reflexes_adds_featac(tmp_path):
    char_dir = write_character(tmp_path, "tester", base_character())

    feat_dictionary = [
        {
            "lightning reflexes": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [1],
            }
        }
    ]
    feat_list = ["lightning reflexes"]

    select_character_feat(
        character="tester",
        feat_name="lightning reflexes",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["featac"] == 2
    assert saved["feats taken"] == ["lightning reflexes"]
    assert saved["hfeats taken"] == ["lightning reflexes"]


def test_select_character_feat_bull_strength_increases_strength_and_recalculates_bonuses(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(strength=5, abhit=2, abdamage=2),
    )

    feat_dictionary = [
        {
            "bull strength": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [2],
            }
        }
    ]
    feat_list = ["bull strength"]

    select_character_feat(
        character="tester",
        feat_name="bull strength",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["strength"] == 7
    assert saved["abhit"] == 3
    assert saved["abdamage"] == 3
    assert saved["feats taken"] == ["bull strength"]
    assert saved["hfeats taken"] == ["bull strength"]
    assert saved["remaining feats"] == 1


def test_select_character_feat_improved_bull_strength_replaces_visible_lower_feat(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(
            level=6,
            strength=7,
            abhit=3,
            abdamage=3,
            **{
                "remaining feats": 1,
                "feats taken": ["bull strength"],
                "hfeats taken": ["bull strength"],
            },
        ),
    )

    feat_dictionary = [
        {
            "improved bull strength": {
                "requirements": [6, 0, 0, 0, "bull strength"],
                "action": [2],
            }
        }
    ]
    feat_list = ["improved bull strength"]

    select_character_feat(
        character="tester",
        feat_name="improved bull strength",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["strength"] == 9
    assert saved["abhit"] == 4
    assert saved["abdamage"] == 4
    assert saved["feats taken"] == ["improved bull strength"]
    assert saved["hfeats taken"] == ["bull strength", "improved bull strength"]
    assert saved["remaining feats"] == 0


def test_select_character_feat_cat_grace_increases_dexterity_and_recalculates_ac_bonus(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(dexterity=5, abac=2),
    )

    feat_dictionary = [
        {
            "cat grace": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [2],
            }
        }
    ]
    feat_list = ["cat grace"]

    select_character_feat(
        character="tester",
        feat_name="cat grace",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["dexterity"] == 7
    assert saved["abac"] == 3
    assert saved["feats taken"] == ["cat grace"]
    assert saved["hfeats taken"] == ["cat grace"]
    assert saved["remaining feats"] == 1


def test_select_character_feat_improved_cat_grace_replaces_visible_lower_feat(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(
            level=6,
            dexterity=7,
            abac=3,
            **{
                "remaining feats": 1,
                "feats taken": ["cat grace"],
                "hfeats taken": ["cat grace"],
            },
        ),
    )

    feat_dictionary = [
        {
            "improved cat grace": {
                "requirements": [6, 0, 0, 0, "cat grace"],
                "action": [2],
            }
        }
    ]
    feat_list = ["improved cat grace"]

    select_character_feat(
        character="tester",
        feat_name="improved cat grace",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["dexterity"] == 9
    assert saved["abac"] == 4
    assert saved["feats taken"] == ["improved cat grace"]
    assert saved["hfeats taken"] == ["cat grace", "improved cat grace"]
    assert saved["remaining feats"] == 0


def test_select_character_feat_bear_endurance_increases_constitution_and_hp_bonus(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(constitution=5, abhp=10),
    )

    feat_dictionary = [
        {
            "bear endurance": {
                "requirements": [1, 0, 0, 0, "none", 0],
                "action": [2],
            }
        }
    ]
    feat_list = ["bear endurance"]

    select_character_feat(
        character="tester",
        feat_name="bear endurance",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["constitution"] == 7
    assert saved["abhp"] == 15
    assert saved["feats taken"] == ["bear endurance"]
    assert saved["hfeats taken"] == ["bear endurance"]
    assert saved["remaining feats"] == 1


def test_select_character_feat_improved_bear_endurance_replaces_visible_lower_feat(tmp_path):
    char_dir = write_character(
        tmp_path,
        "tester",
        base_character(
            level=6,
            constitution=7,
            abhp=15,
            **{
                "remaining feats": 1,
                "feats taken": ["bear endurance"],
                "hfeats taken": ["bear endurance"],
            },
        ),
    )

    feat_dictionary = [
        {
            "improved bear endurance": {
                "requirements": [6, 0, 0, 0, "bear endurance"],
                "action": [2],
            }
        }
    ]
    feat_list = ["improved bear endurance"]

    select_character_feat(
        character="tester",
        feat_name="improved bear endurance",
        feat_list=feat_list,
        feat_dictionary=feat_dictionary,
        character_dir=char_dir,
    )

    saved = load_character("tester", characters_dir=char_dir)
    assert saved["constitution"] == 9
    assert saved["abhp"] == 20
    assert saved["feats taken"] == ["improved bear endurance"]
    assert saved["hfeats taken"] == ["bear endurance", "improved bear endurance"]
    assert saved["remaining feats"] == 0