import json

from src.character_repository import build_character_who_messages


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def make_character(
    *,
    name="Arena Name",
    build="strength",
    level=3,
    wins=4,
    losses=1,
    forfeits=2,
    trait="brawler",
):
    return {
        "name": name,
        "build": build,
        "level": level,
        "wins": wins,
        "losses": losses,
        "forfeits": forfeits,
        "trait": trait,
    }


def test_build_character_who_messages_for_normal_character(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_json(char_folder / "playerDatabase.json", {"Arena Name": "their perfect doll"})
    write_json(
        char_folder / "their perfect doll.json",
        make_character(
            name="Arena Name",
            build="dexterity",
            level=7,
            wins=8,
            losses=2,
            forfeits=3,
            trait="nimble",
        ),
    )

    result = build_character_who_messages(str(char_folder), "their perfect doll")

    assert result == [
        "their perfect doll's character name is: Arena Name, and they are a level: 7 "
        "[color=pink]dexterity[/color] build.",
        "Arena Name's current win/loss score is: [color=pink]8 wins[/color], and "
        "[color=yellow]2 losses[/color]. ([color=red]80%[/color]) "
        "They have also [color=green]forfeited 3 times.[/color]",
    ]


def test_build_character_who_messages_for_cursed_character(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_json(char_folder / "playerDatabase.json", {"Cursed Name": "cursed profile"})
    write_json(
        char_folder / "cursed profile.json",
        make_character(
            name="Cursed Name",
            build="constitution",
            level=5,
            wins=1,
            losses=1,
            forfeits=0,
            trait="cursed",
        ),
    )

    result = build_character_who_messages(str(char_folder), "cursed profile")

    assert result[0] == (
        "cursed profile's character name is: Cursed Name, and they are a level: 5 "
        "[color=pink]constitution[/color] build. They are also [color=cyan]cursed[/color]"
    )


def test_build_character_who_messages_for_zero_total_fights(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_json(char_folder / "playerDatabase.json", {"New Fighter": "new profile"})
    write_json(
        char_folder / "new profile.json",
        make_character(
            name="New Fighter",
            wins=0,
            losses=0,
            forfeits=0,
        ),
    )

    result = build_character_who_messages(str(char_folder), "new profile")

    assert result[1] == (
        "Either New Fighter has a 0% win/loss ratio, or 100%. It all depends "
        "on how you justify a person that has never entered the arena yet."
    )


def test_build_character_who_messages_for_missing_character_sheet(tmp_path):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_json(char_folder / "playerDatabase.json", {"Missing Name": "missing profile"})

    result = build_character_who_messages(str(char_folder), "missing profile")

    assert result == [
        "missing profile isn't a valid name for a character sheet. You are just typing "
        "in their [color=red]profile name.[/color] example: !who <profile name>"
    ]


import json

from original.onMSGUtils import message_4_who


UNSPOILED_OOC = "ADH-8216a753c1ef08445052"
OTHER_ROOM = "ADH-not-the-ooc-room"


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def test_message_4_who_delegates_for_valid_profile(tmp_path, monkeypatch):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    write_json(char_folder / "playerDatabase.json", {"Arena Name": "their perfect doll"})
    write_json(
        char_folder / "their perfect doll.json",
        {
            "name": "Arena Name",
            "build": "strength",
            "level": 4,
            "wins": 3,
            "losses": 1,
            "forfeits": 2,
            "trait": "brawler",
        },
    )

    monkeypatch.chdir(tmp_path)

    result = message_4_who(
        UNSPOILED_OOC,
        str(char_folder),
        UNSPOILED_OOC,
        "!who their perfect doll",
    )

    assert result == [
        "their perfect doll's character name is: Arena Name, and they are a level: 4 "
        "[color=pink]strength[/color] build.",
        "Arena Name's current win/loss score is: [color=pink]3 wins[/color], and "
        "[color=yellow]1 losses[/color]. ([color=red]75%[/color]) "
        "They have also [color=green]forfeited 2 times.[/color]",
    ]


def test_message_4_who_wrong_room_message(tmp_path, monkeypatch):
    char_folder = tmp_path / "characters"
    char_folder.mkdir()

    monkeypatch.chdir(tmp_path)

    result = message_4_who(
        OTHER_ROOM,
        str(char_folder),
        UNSPOILED_OOC,
        "!who their perfect doll",
    )

    assert result == [
        "This Command can only be used in "
        "[session=Unspoiled Desire (Command and OoC Room)]adh-8216a753c1ef08445052[/session]"
    ]