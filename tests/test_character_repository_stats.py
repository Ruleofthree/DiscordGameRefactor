import json

from src.character_repository import assign_character_stats


def write_character(char_dir, profile_name, data):
    path = char_dir / f"{profile_name}.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def read_character(char_dir, profile_name):
    return json.loads((char_dir / f"{profile_name}.json").read_text(encoding="utf-8"))


def base_character(**overrides):
    data = {
        "name": "Test Character",
        "level": 1,
        "build": "strength",
        "strength": 0,
        "dexterity": 0,
        "constitution": 0,
        "ap": 15,
        "reset": 3,
        "abhit": 0,
        "abdamage": 0,
        "abac": 0,
        "abhp": 0,
        "initiative": 0,
    }
    data.update(overrides)
    return data


def test_assign_character_stats_strength_build_writes_stats_and_bonuses(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character(build="strength"))

    msg = assign_character_stats(char_dir, "tester", "!stats 8 4 3")

    data = read_character(char_dir, "tester")

    assert data["strength"] == 8
    assert data["dexterity"] == 4
    assert data["constitution"] == 3
    assert data["abhit"] == 4
    assert data["abdamage"] == 4
    assert data["abac"] == 2
    assert data["abhp"] == 5
    assert data["initiative"] == 2

    assert msg[0] == (
        "Allocating the following: \n\n"
        "Strength: 8   (+4 bonus to hit and 4 to damage.)\n"
        "Dexterity: 4   (+2 bonus to armor class.)\n"
        "Constitution: 3   (+5 bonus to hit points.)\n"
    )


def test_assign_character_stats_dexterity_build_writes_legacy_damage_bonus(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character(build="dexterity"))

    assign_character_stats(char_dir, "tester", "!stats 5 7 3")

    data = read_character(char_dir, "tester")

    assert data["strength"] == 5
    assert data["dexterity"] == 7
    assert data["constitution"] == 3
    assert data["abhit"] == 1
    assert data["abdamage"] == 1
    assert data["abac"] == 3
    assert data["abhp"] == 5
    assert data["initiative"] == 3


def test_assign_character_stats_constitution_build_writes_legacy_damage_bonus(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character(build="constitution"))

    assign_character_stats(char_dir, "tester", "!stats 6 4 5")

    data = read_character(char_dir, "tester")

    assert data["strength"] == 6
    assert data["dexterity"] == 4
    assert data["constitution"] == 5
    assert data["abhit"] == 2
    assert data["abdamage"] == 2
    assert data["abac"] == 2
    assert data["abhp"] == 6
    assert data["initiative"] == 2


def test_assign_character_stats_rejects_missing_character(tmp_path):
    msg = assign_character_stats(tmp_path, "tester", "!stats 5 5 5")

    assert msg == [
        "You don't even have a character created yet. Type !name <name> in the room. "
        "Where <name> is your character's actual name. (Example: !name Joe)"
    ]


def test_assign_character_stats_rejects_already_assigned_stats(tmp_path):
    char_dir = tmp_path
    write_character(
        char_dir,
        "tester",
        base_character(strength=5, dexterity=5, constitution=5),
    )

    msg = assign_character_stats(char_dir, "tester", "!stats 5 5 5")

    assert msg == [
        "You have already set up your character's stats. If you want to change them, you will "
        "need to use the [color=pink]!respec[/color] command."
    ]


def test_assign_character_stats_rejects_missing_build(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character(build=""))

    msg = assign_character_stats(char_dir, "tester", "!stats 5 5 5")

    assert msg == [
        "You need to pick a build path first. Please use the [color=pink]!build[/color] command."
    ]


def test_assign_character_stats_rejects_wrong_total_points(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character(ap=15))

    msg = assign_character_stats(char_dir, "tester", "!stats 5 5 4")

    assert msg == ["Make sure total points used is no more or less than 15."]


def test_assign_character_stats_rejects_level_one_stat_above_ten(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character(level=1))

    msg = assign_character_stats(char_dir, "tester", "!stats 11 2 2")

    assert msg == ["No one stat can be above 10 at this point in time. Please try again."]


def test_assign_character_stats_rejects_negative_stat(tmp_path):
    char_dir = tmp_path
    write_character(char_dir, "tester", base_character())

    msg = assign_character_stats(char_dir, "tester", "!stats -1 8 8")

    assert msg == ["Why would you even try to pick a negative stat? Please try again."]