import json
import os
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CHARACTERS_DIR = PROJECT_ROOT / "characters"


def normalize_character_name(character_name: str) -> str:
    """
    Normalize a character/profile name the same way the legacy bot usually does.

    This intentionally only lowercases and trims outer whitespace.
    It does not replace spaces, remove punctuation, or otherwise sanitize names,
    because legacy character filenames may contain spaces.
    """
    return character_name.strip().lower()


def get_character_path(
    character_name: str,
    characters_dir: Path | str = CHARACTERS_DIR,
) -> Path:
    """
    Return the expected JSON path for a character file.

    The directory is injectable so tests can use tmp_path instead of live data.
    """
    base_dir = Path(characters_dir)
    normalized_name = normalize_character_name(character_name)
    return base_dir / f"{normalized_name}.json"


def character_exists(
    character_name: str,
    characters_dir: Path | str = CHARACTERS_DIR,
) -> bool:
    """
    Return True if the character JSON file exists.
    """
    return get_character_path(character_name, characters_dir).is_file()


def load_character(
    character_name: str,
    characters_dir: Path | str = CHARACTERS_DIR,
) -> dict[str, Any]:
    """
    Load a character JSON file and return its dictionary data.

    Raises FileNotFoundError naturally if the character does not exist.
    Raises json.JSONDecodeError naturally if the file contains invalid JSON.
    """
    character_path = get_character_path(character_name, characters_dir)

    with character_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def delete_character(character, characters_dir):
    characters_path = Path(characters_dir)
    player = character.lower()
    character_file = characters_path / f"{player}.json"
    player_database_file = characters_path / "playerDatabase.json"

    with player_database_file.open("r", encoding="utf-8") as file:
        player_database = json.loads(file.read())

    name = ""
    for database_name, database_player in player_database.items():
        if database_player == player:
            name = database_name

    player_database.pop(name, None)

    with player_database_file.open("w", encoding="utf-8") as file:
        json.dump(player_database, file, sort_keys=True, indent=2)

    try:
        character_file.unlink()
        return f"{name} has been erased."
    except FileNotFoundError:
        return "You don't have a character to delete."


def save_character(
    character_name: str,
    character_data: dict[str, Any],
    characters_dir: Path | str = CHARACTERS_DIR,
) -> None:
    """
    Save character dictionary data to the character JSON file.

    This creates the character directory if needed, which keeps tests simple
    and makes the helper safer for future character creation work.
    """
    character_path = get_character_path(character_name, characters_dir)
    character_path.parent.mkdir(parents=True, exist_ok=True)

    with character_path.open("w", encoding="utf-8") as file:
        json.dump(character_data, file, ensure_ascii=False, indent=2)


def create_character(character, name, char_folder):
    character = character.lower()
    char_folder = Path(char_folder)
    character_file = char_folder / f"{character}.json"

    if character_file.is_file():
        return False

    with open(char_folder / "levelchart.json", "r", encoding="utf-8") as file:
        level_dict = json.load(file)

    level = 1
    xp = 0

    character_data = {}
    character_data["name"] = name
    character_data["level"] = level
    character_data["build"] = ""
    character_data["trait"] = ""
    character_data["hp"] = level_dict["1"][0]
    character_data["total feats"] = level_dict["1"][4]
    character_data["base damage"] = str(level_dict["1"][1]) + "d" + str(level_dict["1"][2])
    character_data["hit"] = level_dict["1"][5]
    character_data["damage"] = level_dict["1"][5]
    character_data["ac"] = level_dict["1"][6]
    character_data["currentxp"] = xp
    character_data["nextlevel"] = level_dict["1"][7]
    character_data["strength"] = 0
    character_data["dexterity"] = 0
    character_data["constitution"] = 0
    character_data["remaining feats"] = 2
    character_data["ap"] = level_dict["1"][3]
    character_data["apboost"] = False
    character_data["regeneration"] = 0
    character_data["feats taken"] = []
    character_data["armor"] = {"armor1": "n/a", "armor2": "n/a", "armor3": "n/a"}
    character_data["equip"] = ""
    character_data["hfeats taken"] = []
    character_data["reset"] = 3
    character_data["wins"] = 0
    character_data["losses"] = 0
    character_data["forfeits"] = 0
    character_data["abhp"] = 0
    character_data["abhit"] = 0
    character_data["abdamage"] = 0
    character_data["abac"] = 0
    character_data["feathp"] = 0
    character_data["feathit"] = 0
    character_data["featdamage"] = 0
    character_data["featac"] = 0
    character_data["thp"] = 0
    character_data["tac"] = 0
    character_data["thit"] = 0
    character_data["tdamage"] = 0
    character_data["tdr"] = 0
    character_data["dexfighter"] = 0
    character_data["renown"] = 0
    character_data["initiative"] = 0
    character_data["potions"] = []
    character_data["potioneffect"] = ""
    character_data["potionhit"] = 0
    character_data["potiondamage"] = 0
    character_data["potionac"] = 0
    character_data["potionhp"] = 0
    character_data["potionblur"] = 0
    character_data["potionstr"] = 0
    character_data["potiondex"] = 0
    character_data["potioncon"] = 0
    character_data["potionregen"] = 0
    character_data["pstrength"] = 0
    character_data["pdexterity"] = 0
    character_data["pconstitution"] = 0
    character_data["armorhit"] = 0
    character_data["armordamage"] = 0
    character_data["armorac"] = 0
    character_data["armorhp"] = 0
    character_data["armordr"] = 0
    character_data["armorstrength"] = 0
    character_data["armordexterity"] = 0
    character_data["armorconstitution"] = 0
    character_data["armorblur"] = 0
    character_data["armorinitiative"] = 0
    character_data["blur"] = 0
    character_data["traithit"] = 0
    character_data["traitdamage"] = 0
    character_data["traitac"] = 0
    character_data["traitdr"] = 0
    character_data["traithp"] = 0
    character_data["traitregen"] = 0
    character_data["cursed"] = 0
    character_data["status"] = ""
    character_data["statuscounter"] = 0
    character_data["fight"] = 0

    with open(character_file, "w", encoding="utf-8") as file:
        json.dump(character_data, file, ensure_ascii=False, indent=2)

    with open(char_folder / "playerDatabase.json", "r", encoding="utf-8") as file:
        player_database = json.load(file)

    player_database[name] = character

    with open(char_folder / "playerDatabase.json", "w", encoding="utf-8") as file:
        json.dump(player_database, file, sort_keys=True, indent=2)

    return True

def select_character_build(character: str, build: str, characters_dir: Path | str = CHARACTERS_DIR) -> str:
    characters_path = Path(characters_dir)
    character_path = characters_path / f"{character.lower()}.json"

    with character_path.open("r+", encoding="utf-8") as file:
        character_data = json.load(file)

        if character_data["build"] == "":
            if build == "strength":
                character_data["build"] = build

                if character_data["level"] <= 3:
                    character_data["feats taken"].append("focus")

            elif build == "dexterity":
                character_data["build"] = build

            elif build == "constitution":
                character_data["build"] = build

            msg = (
                "You have identified your character as a " + build
                + " build, and it has been recorded as such in your character sheet. "
                "Please ues [color=pink]!stats[/color] command to select your stat points, "
                "before selecting feats."
            )
        else:
            msg = "You already have selected a build."

        file.seek(0)
        file.write(json.dumps(character_data, ensure_ascii=False, indent=2))
        file.truncate()

    return msg


def list_characters_by_level(level: int, characters_dir: Path | str = CHARACTERS_DIR) -> list[str]:
    characters_path = Path(characters_dir)
    matching_profiles = []

    with (characters_path / "playerDatabase.json").open("r", encoding="utf-8") as file:
        player_database = json.loads(file.read())

    for profile_name in player_database.values():
        character_path = characters_path / f"{profile_name}.json"

        with character_path.open("r+", encoding="utf-8") as file:
            character_data = json.load(file)

        if character_data["level"] == level:
            matching_profiles.append(profile_name)

    return matching_profiles


def assign_character_stats(char_dir, character, message):
    char_dir = Path(char_dir)
    char_file = char_dir / f"{character.lower()}.json"

    msg = []

    info = message.split(" ")
    strength = int(info[1])
    dexterity = int(info[2])
    constitution = int(info[3])

    if not char_file.is_file():
        msg.append(
            "You don't even have a character created yet. Type !name <name> in the room. "
            "Where <name> is your character's actual name. (Example: !name Joe)"
        )
        return msg

    with char_file.open("r", encoding="utf-8") as file:
        char_data = json.load(file)

    ap = char_data["ap"]
    build = char_data["build"]
    level = char_data["level"]

    if (
        char_data["strength"] != 0
        and char_data["dexterity"] != 0
        and char_data["constitution"] != 0
    ):
        msg.append(
            "You have already set up your character's stats. If you want to change them, you will "
            "need to use the [color=pink]!respec[/color] command."
        )
        return msg

    if build == "":
        msg.append("You need to pick a build path first. Please use the [color=pink]!build[/color] command.")
        return msg

    total = strength + dexterity + constitution

    if total > ap or total < ap:
        msg.append("Make sure total points used is no more or less than " + str(ap) + ".")
        return msg

    if (strength > 10 or dexterity > 10 or constitution > 10) and level in [1, 2, 3, 4]:
        msg.append("No one stat can be above 10 at this point in time. Please try again.")
        return msg

    if (strength > 11 or dexterity > 11 or constitution > 11) and level in [5, 6, 7, 8, 9]:
        msg.append("No one stat can be above 11 at this point in time. Please try again.")
        return msg

    if (strength > 12 or dexterity > 12 or constitution > 12) and level in [10, 11, 12, 13, 14]:
        msg.append("No one stat can be above 12 at this point in time. Please try again.")
        return msg

    if (strength > 13 or dexterity > 13 or constitution > 13) and level in [15, 16, 17, 18, 19]:
        msg.append("No one stat can be above 13 at this point in time. Please try again.")
        return msg

    if (strength > 14 or dexterity > 14 or constitution > 14) and level == 20:
        msg.append("No one stat can be above 14 at this point in time. Please try again.")
        return msg

    if strength < 0 or dexterity < 0 or constitution < 0:
        msg.append("Why would you even try to pick a negative stat? Please try again.")
        return msg

    hit_mod = 0

    if build == "strength":
        hit_mod = int(strength / 2)
        str_mod = int(strength / 2)
        dex_mod = int(dexterity / 2)
        con_mod = int(constitution / 2) * 5
    elif build == "dexterity":
        str_mod = int(strength / 5)
        dex_mod = int(dexterity / 2)
        con_mod = int(constitution / 2) * 5
    elif build == "constitution":
        str_mod = int(strength / 3)
        dex_mod = int(dexterity / 2)
        con_mod = int(constitution / 2) * 3

    msg.append(
        "Allocating the following: \n\nStrength: " + str(strength) +
        "   (+" + str(hit_mod) + " bonus to hit and " +
        str(str_mod) + " to damage.)\nDexterity: " +
        str(dexterity) + "   (+" + str(dex_mod) + " bonus to armor class.)\n"
        "Constitution: " + str(constitution) + "   (+" + str(con_mod) + " bonus to hit points.)\n"
    )

    msg.append(
        "The above points have been placed on your character sheet. Please "
        "type [color=pink]!viewchar[/color] to see your character sheet. "
        "You need to chose two feats, and a trait as well. Type [color=pink]!featlist[/color] "
        "to see a list of feats. Type [color=pink]!feathelp <feat name>[/color], "
        "to get help on a specific feat, or type "
        "[color=pink]!featpick <feat name>[/color] to choose that feat. To see a list of traits, "
        "use [color=pink]!traitlist[/color], use [color=pink]!traithelp <trait name>[/color] for its "
        "description and use [color=pink]!traitpick <trait name>[/color] to select that trait."
    )

    char_data["strength"] = int(strength)
    char_data["dexterity"] = int(dexterity)
    char_data["constitution"] = int(constitution)
    char_data["abhit"] = str_mod
    char_data["abdamage"] = str_mod
    char_data["abac"] = dex_mod
    char_data["abhp"] = con_mod
    char_data["initiative"] = dex_mod

    with char_file.open("w", encoding="utf-8") as file:
        json.dump(char_data, file, ensure_ascii=False, indent=2)

    return msg


def select_character_trait(char_folder, character, message, trait_list, trait_dictionary, trait):
    char_folder = Path(char_folder)
    character_file = char_folder / f"{character.lower()}.json"

    with character_file.open("r", encoding="utf-8") as char_sheet:
        char_data = json.load(char_sheet)

    regeneration = char_data["traitregen"]
    brawler = char_data["traithit"]
    thug = char_data["traitdamage"]
    nimble = char_data["traitac"]
    hearty = char_data["traithp"]
    thickskinned = char_data["traitdr"]
    opportunist = char_data["initiative"]
    nebulous = char_data["blur"]
    strength = char_data["strength"]
    dexterity = char_data["dexterity"]
    constitution = char_data["constitution"]

    if char_data["trait"] != "":
        return "You've already selected a trait. If you wish to change it, you must !respec if you have the points."

    if strength >= 0 and dexterity >= 0 and constitution >= 0:
        with character_file.open("r+", encoding="utf-8") as file:
            char_data = json.load(file)

            if trait in trait_list:
                level = char_data["level"]
                char_data["trait"] = trait

                if trait == "cursed" and level in range(1, 5):
                    cursed = trait_dictionary[0]["cursed"]["bonus"][0]
                    char_data["cursed"] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == "cursed" and level in range(5, 10):
                    cursed = trait_dictionary[0]["cursed"]["bonus"][1]
                    char_data["cursed"] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == "cursed" and level in range(10, 15):
                    cursed = trait_dictionary[0]["cursed"]["bonus"][2]
                    char_data["cursed"] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == "cursed" and level in range(15, 20):
                    cursed = trait_dictionary[0]["cursed"]["bonus"][3]
                    char_data["cursed"] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."
                elif trait == "cursed" and level == 20:
                    cursed = trait_dictionary[0]["cursed"]["bonus"][4]
                    char_data["cursed"] = cursed
                    msg = "The trait 'cursed' has been added to your character sheet."

                if char_data["tdr"] == 0:
                    if trait == "regeneration" and level in range(1, 5):
                        regeneration = trait_dictionary[0]["regeneration"]["bonus"][0]
                        char_data["traitregen"] = regeneration
                        msg = "The trait Regeneration' has been added to your character sheet."
                    elif trait == "regeneration" and level in range(5, 10):
                        regeneration = trait_dictionary[0]["regeneration"]["bonus"][1]
                        char_data["traitregen"] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                    elif trait == "regeneration" and level in range(10, 15):
                        regeneration = trait_dictionary[0]["regeneration"]["bonus"][2]
                        char_data["traitregen"] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                    elif trait == "regeneration" and level in range(15, 20):
                        regeneration = trait_dictionary[0]["regeneration"]["bonus"][3]
                        char_data["traitregen"] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                    elif trait == "regeneration" and level == 20:
                        regeneration = trait_dictionary[0]["regeneration"]["bonus"][4]
                        char_data["traitregen"] = regeneration
                        msg = "The trait 'Regeneration' has been added to your character sheet."
                else:
                    msg = "You can not take regeneration as you have a non-zero value for Damage Reduction"

                if trait == "brawler" and level in range(1, 5):
                    brawler = trait_dictionary[0]["brawler"]["bonus"][0]
                    char_data["traithit"] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == "brawler" and level in range(5, 10):
                    brawler = trait_dictionary[0]["brawler"]["bonus"][1]
                    char_data["traithit"] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == "bralwer" and level in range(10, 15):
                    brawler = trait_dictionary[0]["brawler"]["bonus"][2]
                    char_data["traithit"] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == "brawler" and level in range(15, 20):
                    brawler = trait_dictionary[0]["brawler"]["bonus"][3]
                    char_data["traithit"] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."
                elif trait == "brawler" and level == 20:
                    brawler = trait_dictionary[0]["brawler"]["bonus"][4]
                    char_data["traithit"] = brawler
                    msg = "The trait 'Brawler' has been added to your character sheet."

                if trait == "thug" and level in range(1, 5):
                    thug = trait_dictionary[0]["thug"]["bonus"][0]
                    char_data["traitdamage"] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == "thug" and level in range(5, 10):
                    thug = trait_dictionary[0]["thug"]["bonus"][1]
                    char_data["traitdamage"] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == "thug" and level in range(10, 15):
                    thug = trait_dictionary[0]["thug"]["bonus"][2]
                    char_data["traitdamage"] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == "thug" and level in range(15, 20):
                    thug = trait_dictionary[0]["thug"]["bonus"][3]
                    char_data["traitdamage"] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."
                elif trait == "thug" and level == 20:
                    thug = trait_dictionary[0]["thug"]["bonus"][4]
                    char_data["traitdamage"] = thug
                    msg = "The trait 'Thug' has been added to your character sheet."

                if trait == "hearty" and level in range(1, 5):
                    hearty = trait_dictionary[0]["hearty"]["bonus"][0]
                    char_data["traithp"] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == "hearty" and level in range(5, 10):
                    hearty = trait_dictionary[0]["hearty"]["bonus"][1]
                    char_data["traithp"] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == "hearty" and level in range(10, 15):
                    hearty = trait_dictionary[0]["hearty"]["bonus"][2]
                    char_data["traithp"] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == "hearty" and level in range(15, 20):
                    hearty = trait_dictionary[0]["hearty"]["bonus"][3]
                    char_data["traithp"] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."
                elif trait == "hearty" and level == 20:
                    hearty = trait_dictionary[0]["hearty"]["bonus"][4]
                    char_data["traithp"] = hearty
                    msg = "The trait 'Hearty' has been added to your character sheet."

                if trait == "nimble" and level in range(1, 5):
                    nimble = trait_dictionary[0]["nimble"]["bonus"][0]
                    char_data["traitac"] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == "nimble" and level in range(5, 10):
                    nimble = trait_dictionary[0]["nimble"]["bonus"][1]
                    char_data["traitac"] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == "nimble" and level in range(10, 15):
                    nimble = trait_dictionary[0]["nimble"]["bonus"][2]
                    char_data["traitac"] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == "nimble" and level in range(15, 20):
                    nimble = trait_dictionary[0]["nimble"]["bonus"][3]
                    char_data["traitac"] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."
                elif trait == "nimble" and level == 20:
                    nimble = trait_dictionary[0]["nimble"]["bonus"][4]
                    char_data["traitac"] = nimble
                    msg = "The trait 'Nimble' has been added to your character sheet."

                if char_data["regeneration"] == 0:
                    if trait == "thickskinned" and level in range(1, 5):
                        thickskinned = trait_dictionary[0]["thickskinned"]["bonus"][0]
                        char_data["traitdr"] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == "thickskinned" and level in range(5, 10):
                        thickskinned = trait_dictionary[0]["thickskinned"]["bonus"][1]
                        char_data["traitdr"] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == "thickskinned" and level in range(10, 15):
                        thickskinned = trait_dictionary[0]["thickskinned"]["bonus"][2]
                        char_data["traitdr"] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == "thickskinned" and level in range(15, 20):
                        thickskinned = trait_dictionary[0]["thickskinned"]["bonus"][3]
                        char_data["traitdr"] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                    elif trait == "thickskinned" and level == 20:
                        thickskinned = trait_dictionary[0]["thickskinned"]["bonus"][4]
                        char_data["traitdr"] = thickskinned
                        msg = "The trait 'Thickskinned' has been added to your character sheet."
                else:
                    msg = "You can not take thickskinned as you have a non-zero value for regeneration"

                if trait == "opportunist" and level in range(1, 5):
                    opportunist = trait_dictionary[0]["opportunist"]["bonus"][0]
                    char_data["initiative"] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == "opportunist" and level in range(5, 10):
                    opportunist = trait_dictionary[0]["opportunist"]["bonus"][1]
                    char_data["initiative"] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == "opportunist" and level in range(10, 15):
                    opportunist = trait_dictionary[0]["opportunist"]["bonus"][2]
                    char_data["initiative"] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == "opportunist" and level in range(15, 20):
                    opportunist = trait_dictionary[0]["opportunist"]["bonus"][3]
                    char_data["initiative"] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."
                elif trait == "opportunist" and level == 20:
                    opportunist = trait_dictionary[0]["opportunist"]["bonus"][4]
                    char_data["initiative"] = opportunist
                    msg = "The trait 'Opportunist' has been added to your character sheet."

                if trait == "nebulous" and level in range(1, 5):
                    nebulous = trait_dictionary[0]["nebulous"]["bonus"][0]
                    char_data["blur"] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == "nebulous" and level in range(5, 10):
                    nebulous = trait_dictionary[0]["nebulous"]["bonus"][1]
                    char_data["blur"] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == "nebulous" and level in range(10, 15):
                    nebulous = trait_dictionary[0]["nebulous"]["bonus"][2]
                    char_data["blur"] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == "nebulous" and level in range(15, 20):
                    nebulous = trait_dictionary[0]["nebulous"]["bonus"][3]
                    char_data["blur"] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."
                elif trait == "nebulous" and level == 20:
                    nebulous = trait_dictionary[0]["nebulous"]["bonus"][4]
                    char_data["blur"] = nebulous
                    msg = "The trait 'Nebulous' has been added to your character sheet."

                file.seek(0)
                file.write(json.dumps(char_data, ensure_ascii=False, indent=2))
                file.truncate()
                return msg

            if trait not in trait_list:
                return message + " is not a trait. Please use [color=pink]!traitlist[/color] for a list ot traits."

            return "You need to set up your stats first, before selecting a trait. please use the !stats command."

    return "You need to set up your stats first, before selecting a trait. please use the !stats command."


def select_character_feat(character, feat_name, feat_list, feat_dictionary, character_dir=None):
    msg = []

    char_data = load_character(character, characters_dir=character_dir)

    level = char_data["level"]
    build = char_data["build"]
    strength = char_data["strength"]
    dexterity = char_data["dexterity"]
    constitution = char_data["constitution"]
    remaining_feats = char_data["remaining feats"]
    has_taken = char_data["feats taken"]
    hidden_taken = char_data["hfeats taken"]
    ap = char_data["ap"]

    total = strength + dexterity + constitution

    toggle_feat = ["defensive fighting", "power attack", "masochist"]
    str_only = [
        "hurt me",
        "improved hurt me",
        "greater hurt me",
        "hurt me more",
        "bullrush",
        "improved bullrush",
        "greater bullrush",
    ]
    dex_only = [
        "evasion",
        "improved evasion",
        "greater evasion",
        "cheap shot",
        "improved cheap shot",
        "greater cheap shot",
    ]
    con_only = [
        "deaths door",
        "improved deaths door",
        "greater deaths door",
        "inner strength",
        "improved inner strength",
        "greater inner strength",
    ]
    nope = ["focus", "improved focus", "greater focus", "perfect focus"]

    answer = feat_name.lower()

    if total < ap:
        msg.append("Please select your character stats with the [color=pink]!stats[/color] command first.")
    elif (
        answer in str_only and build != "strength"
        or answer in dex_only and build != "dexterity"
        or answer in con_only and build != "constitution"
    ):
        msg.append("This feat is not available for your build choice.")
    elif answer in toggle_feat and (
        "defensive fighting" in has_taken
        or "power attack" in has_taken
        or "masochist" in has_taken
    ):
        msg.append(
            "You can not take more than one toggle feat. You already have either [color=yellow]Power "
            "Attack[/color], [color=yellow]Defensive Fighting[/color], or [color=yellow]Masochist[/color]."
        )
    elif answer in nope:
        msg.append(
            "This feat is given to strength builds automatically at levels 3/9/15/18, and can not be taken "
            "in any other fashion"
        )
    elif remaining_feats == 0:
        msg.append("You have no feat slots left to select a new feat")
    elif answer in hidden_taken:
        msg.append("Why are you trying to take a weaker feat than the one you already have? No.")
    elif answer not in feat_list:
        msg.append("Make sure you have spelled the feat correctly")
    else:
        req_level = feat_dictionary[0][answer]["requirements"][0]
        req_feats = feat_dictionary[0][answer]["requirements"][4]

        if req_level > level:
            msg.append("You are not the required level for this feat.")
        elif req_feats not in has_taken and req_feats != "none":
            msg.append("You do hot have the required prerequisites to take this feat.")
        elif answer not in has_taken:
            msg.append(answer + " has been added to your character sheet.")
            msg.append(
                "Make sure you use [color=pink]!viewchar[/color] to ensure you are "
                "obtaining proper bonuses during fights."
            )

            remaining_feats -= 1
            hidden_taken.append(answer)
            has_taken.append(answer)
            if answer == "bull strength":
                char_data["strength"] = char_data["strength"] + 2
                char_data["abhit"] = int(char_data["strength"] / 2)
                char_data["abdamage"] = int(char_data["strength"] / 2)

            if answer == "improved bull strength":
                char_data["strength"] = char_data["strength"] + 2
                char_data["abhit"] = int(char_data["strength"] / 2)
                char_data["abdamage"] = int(char_data["strength"] / 2)
                index = has_taken.index("bull strength")
                has_taken.pop(index)

            if answer == "greater bull strength":
                char_data["strength"] = char_data["strength"] + 2
                char_data["abhit"] = int(char_data["strength"] / 2)
                char_data["abdamage"] = int(char_data["strength"] / 2)
                index = has_taken.index("improved bull strength")
                has_taken.pop(index)

            if answer == "cat grace":
                char_data["dexterity"] = char_data["dexterity"] + 2
                char_data["abac"] = int(char_data["dexterity"] / 2)

            if answer == "improved cat grace":
                char_data["dexterity"] = char_data["dexterity"] + 2
                char_data["abac"] = int(char_data["dexterity"] / 2)
                index = has_taken.index("cat grace")
                has_taken.pop(index)

            if answer == "greater cat grace":
                char_data["dexterity"] = char_data["dexterity"] + 2
                char_data["abac"] = int(char_data["dexterity"] / 2)
                index = has_taken.index("improved cat grace")
                has_taken.pop(index)

            if answer == "bear endurance":
                char_data["constitution"] = char_data["constitution"] + 2
                char_data["abhp"] = char_data["abhp"] + 5

            if answer == "improved bear endurance":
                char_data["constitution"] = char_data["constitution"] + 2
                char_data["abhp"] = char_data["abhp"] + 5
                index = has_taken.index("bear endurance")
                has_taken.pop(index)

            if answer == "greater bear endurance":
                char_data["constitution"] = char_data["constitution"] + 2
                char_data["abhp"] = char_data["abhp"] + 5
                index = has_taken.index("improved bear endurance")
                has_taken.pop(index)

            if answer == "crushing blow":
                char_data["featdamage"] += 2

            if answer == "improved crushing blow":
                char_data["featdamage"] += 2
                index = has_taken.index("crushing blow")
                has_taken.pop(index)

            if answer == "greater crushing blow":
                char_data["featdamage"] += 2
                index = has_taken.index("improved crushing blow")
                has_taken.pop(index)

            if answer == "precision strike":
                char_data["feathit"] += 2

            if answer == "improved precision strike":
                char_data["feathit"] += 2
                index = has_taken.index("precision strike")
                has_taken.pop(index)

            if answer == "greater precision strike":
                char_data["feathit"] += 2
                index = has_taken.index("improved precision strike")
                has_taken.pop(index)

            if answer == "lightning reflexes":
                char_data["featac"] += 2

            if answer == "improved lightning reflexes":
                char_data["featac"] += 2
                index = has_taken.index("lightning reflexes")
                has_taken.pop(index)

            if answer == "greater lightning reflexes":
                char_data["featac"] += 2
                index = has_taken.index("improved lightning reflexes")
                has_taken.pop(index)

            char_data["remaining feats"] = remaining_feats

            if answer == "improved deflect":
                index = has_taken.index("deflect")
                has_taken.pop(index)

            if answer == "greater deflect":
                index = has_taken.index("improved deflect")
                has_taken.pop(index)

            if answer == "improved hurt me":
                index = has_taken.index("hurt me")
                has_taken.pop(index)

            if answer == "greater hurt me":
                index = has_taken.index("improved hurt me")
                has_taken.pop(index)

            if answer == "hurt me more":
                index = has_taken.index("greater hurt me")
                has_taken.pop(index)

            if answer == "improved reckless abandon":
                index = has_taken.index("reckless abandon")
                has_taken.pop(index)

            if answer == "greater reckless abandon":
                index = has_taken.index("improved reckless abandon")
                has_taken.pop(index)

            if answer == "improved deaths door":
                index = has_taken.index("deaths door")
                has_taken.pop(index)

            if answer == "greater deaths door":
                index = has_taken.index("improved deaths door")
                has_taken.pop(index)

            if answer == "improved vile touch":
                index = has_taken.index("vile touch")
                has_taken.pop(index)

            if answer == "greater vile touch":
                index = has_taken.index("improved vile touch")
                has_taken.pop(index)

            if answer == "death touch":
                index = has_taken.index("greater vile touch")
                has_taken.pop(index)

            if answer == "improved heavy hand":
                index = has_taken.index("heavy hand")
                has_taken.pop(index)

            if answer == "greater heavy hand":
                index = has_taken.index("improved heavy hand")
                has_taken.pop(index)

            if answer == "improved evasion":
                index = has_taken.index("evasion")
                has_taken.pop(index)

            if answer == "greater evasion":
                index = has_taken.index("improved evasion")
                has_taken.pop(index)

            if answer == "improved quick strike":
                index = has_taken.index("quick strike")
                has_taken.pop(index)

            if answer == "greater quick strike":
                index = has_taken.index("improved quick strike")
                has_taken.pop(index)

            if answer == "riposte":
                index = has_taken.index("greater quick strike")
                has_taken.pop(index)

            char_data["feats taken"] = has_taken
            char_data["hfeats taken"] = hidden_taken

            save_character(character, char_data, characters_dir=character_dir)

    return msg


def calculate_character_view_totals(char_data):
    build = char_data["build"]

    strength = (
        char_data["strength"]
        + char_data["pstrength"]
        + char_data["armorstrength"]
        + char_data["potionstr"]
    )
    dexterity = (
        char_data["dexterity"]
        + char_data["pdexterity"]
        + char_data["armordexterity"]
        + char_data["potiondex"]
    )
    constitution = (
        char_data["constitution"]
        + char_data["pconstitution"]
        + char_data["armorconstitution"]
        + char_data["potioncon"]
    )

    ac = char_data["ac"]

    if build == "constitution":
        thp = (
            char_data["hp"]
            + char_data["feathp"]
            + char_data["armorhp"]
            + char_data["potionhp"]
            + char_data["traithp"]
            + int(int(constitution / 2) * 3)
        )
        thit = (
            char_data["hit"]
            + char_data["feathit"]
            + char_data["armorhit"]
            + char_data["traithit"]
            - char_data["cursed"]
            + int((strength + constitution) / 2.4)
        )
        tdamage = (
            char_data["damage"]
            + char_data["featdamage"]
            + char_data["armordamage"]
            - char_data["cursed"]
            + char_data["traitdamage"]
            + int(thp / 15)
            + int(strength / 5)
        )
        ac += 4

    elif build == "dexterity":
        thp = (
            char_data["hp"]
            + char_data["feathp"]
            + char_data["armorhp"]
            + char_data["potionhp"]
            + char_data["traithp"]
            + int(int(constitution / 2) * 5)
        )
        thit = (
            char_data["hit"]
            + char_data["feathit"]
            + char_data["armorhit"]
            + char_data["traithit"]
            - char_data["cursed"]
            + int(dexterity / 1.5)
        )
        tdamage = (
            char_data["damage"]
            + char_data["featdamage"]
            + char_data["armordamage"]
            + char_data["traitdamage"]
            - char_data["cursed"]
            + int(dexterity / 4)
            + int(strength / 5)
        )

    else:
        thit = (
            char_data["hit"]
            + char_data["feathit"]
            + char_data["armorhit"]
            + char_data["traithit"]
            - char_data["cursed"]
            + int(strength / 2)
        )
        tdamage = (
            char_data["damage"]
            + char_data["featdamage"]
            + char_data["armordamage"]
            - char_data["cursed"]
            + char_data["traitdamage"]
            + int(strength / 1.5)
        )
        thp = (
            char_data["hp"]
            + char_data["feathp"]
            + char_data["armorhp"]
            + char_data["potionhp"]
            + char_data["traithp"]
            + int(int(constitution / 2) * 5)
        )
        ac += 2

    tac = (
        ac
        + char_data["featac"]
        + char_data["armorac"]
        + char_data["traitac"]
        - char_data["cursed"]
        + int(dexterity / 2)
    )
    tdr = char_data["armordr"] + char_data["traitdr"]
    regen = char_data["traitregen"] + char_data["potionregen"]
    blur = char_data["potionblur"] + char_data["armorblur"] + char_data["blur"]
    initiative = int(dexterity / 2) + char_data["armorinitiative"]

    return {
        "strength": strength,
        "dexterity": dexterity,
        "constitution": constitution,
        "thp": thp,
        "tac": tac,
        "tdr": tdr,
        "thit": thit,
        "tdamage": tdamage,
        "regeneration": regen,
        "blur": blur,
        "initiative": initiative,
    }


def format_character_view_armor_inventory(char_data):
    key_dict = []
    for key in char_data["armor"]:
        key_dict.append(key)

    armor_one = key_dict[0]
    armor_two = key_dict[1]
    armor_three = key_dict[2]

    armor_inv_one = "n/a"
    armor_inv_two = "n/a"
    armor_inv_three = "n/a"

    if char_data["armor"][armor_one] != "n/a":
        equipprice = int(char_data["armor"][armor_one][-1] / 2)
        del char_data["armor"][armor_one][-1]
        armor_inv_one = (
            ", ".join(char_data["armor"][armor_one])
            + " Selling Value: [color=yellow]"
            + str(equipprice)
            + "[/color] renown"
        )

    if char_data["armor"][armor_two] != "n/a":
        equipprice = int(char_data["armor"][armor_two][-1] / 2)
        del char_data["armor"][armor_two][-1]
        armor_inv_two = (
            ", ".join(char_data["armor"][armor_two])
            + " Selling Value: [color=yellow]"
            + str(equipprice)
            + "[/color] rewnown"
        )

    if char_data["armor"][armor_three] != "n/a":
        equipprice = int(char_data["armor"][armor_three][-1] / 2)
        del char_data["armor"][armor_three][-1]
        armor_inv_three = (
            ", ".join(char_data["armor"][armor_three])
            + " Selling Value: [color=yellow]"
            + str(equipprice)
            + "[/color] renown"
        )

    return armor_one, armor_two, armor_three, armor_inv_one, armor_inv_two, armor_inv_three


def format_character_view_potion_inventory(char_data):
    return ", ".join(char_data["potions"])


def build_character_view_context(char_data):
    totals = calculate_character_view_totals(char_data)

    armor_one, armor_two, armor_three, armor_inv_one, armor_inv_two, armor_inv_three = (
        format_character_view_armor_inventory(char_data)
    )

    potion_inventory = format_character_view_potion_inventory(char_data)

    return {
        "totals": totals,
        "armor_one": armor_one,
        "armor_two": armor_two,
        "armor_three": armor_three,
        "armor_inv_one": armor_inv_one,
        "armor_inv_two": armor_inv_two,
        "armor_inv_three": armor_inv_three,
        "potion_inventory": potion_inventory,
    }


def build_character_view_context(char_data):
    totals = calculate_character_view_totals(char_data)

    armor_one, armor_two, armor_three, armor_inv_one, armor_inv_two, armor_inv_three = (
        format_character_view_armor_inventory(char_data)
    )

    potion_inventory = format_character_view_potion_inventory(char_data)

    return {
        "totals": totals,

        "armor_one": armor_one,
        "armor_two": armor_two,
        "armor_three": armor_three,
        "armor_inv_one": armor_inv_one,
        "armor_inv_two": armor_inv_two,
        "armor_inv_three": armor_inv_three,

        "potion_inventory": potion_inventory,

        "equip": char_data["equip"],
        "name": char_data["name"],
        "build": char_data["build"],
        "trait": char_data["trait"],
        "level": char_data["level"],
        "total_feats": char_data["total feats"],
        "base_damage": char_data["base damage"],
        "renown": char_data["renown"],
        "current_xp": char_data["currentxp"],
        "next_level": char_data["nextlevel"],
        "remaining_feats": char_data["remaining feats"],
        "feats_taken": ", ".join(char_data["feats taken"]),
        "ap": char_data["ap"],
        "reset": char_data["reset"],
        "wins": char_data["wins"],
        "losses": char_data["losses"],
        "forfeits": char_data["forfeits"],
        "potion_effect": char_data["potioneffect"],
        "permanent_strength": char_data["pstrength"],
        "permanent_dexterity": char_data["pdexterity"],
        "permanent_constitution": char_data["pconstitution"],
    }


def apply_character_view_totals(char_data, totals):
    char_data["thp"] = totals["thp"]
    char_data["tac"] = totals["tac"]
    char_data["tdr"] = totals["tdr"]
    char_data["thit"] = totals["thit"]
    char_data["tdamage"] = totals["tdamage"]
    char_data["initiative"] = totals["initiative"]
    char_data["regeneration"] = totals["regeneration"]
    return char_data


def add_ability_point(char_data: dict, ability: str) -> tuple[dict, list[str]]:
    msg = []

    valid_abilities = ["str", "strength", "dex", "dexterity", "con", "constitution"]

    if ability not in valid_abilities:
        msg.append(
            "You need to specify the ability you want to point the point to. "
            "Type '!add str' or '!add strength' for strength, and so on."
        )
        return char_data, msg

    if not char_data["apboost"]:
        msg.append("You do not have any more ability points to spend.")
        return char_data, msg

    char_data["apboost"] = False

    if ability == "strength" or ability == "str":
        char_data["strength"] += 1
        msg.append(
            "You have added an ability point to Strength. Please do a [color=pink]!viewchar[/color] "
            "to ensure changes."
        )

    if ability == "dexterity" or ability == "dex":
        char_data["dexterity"] += 1
        msg.append(
            "You have added an ability point to Dexterity. Please do a [color=pink]!viewchar[/color] "
            "to ensure changes."
        )

    if ability == "constitution" or ability == "con":
        char_data["constitution"] += 1
        msg.append(
            "You have added an ability point to Constitution. Please do a [color=pink]!viewchar[/color] "
            "to ensure changes."
        )

    return char_data, msg


def build_character_who_messages(char_folder, profile):
    profile = profile.lower()
    msg = []

    player_database_path = os.path.join(char_folder, "playerDatabase.json")

    with open(player_database_path, "r", encoding="utf-8") as file:
        player_database = json.loads(file.read())

    name = ""
    for item in player_database.items():
        if item[1] == profile:
            name = item[0]

    try:
        character_path = os.path.join(char_folder, profile + ".json")

        with open(character_path, "r+", encoding="utf-8") as file:
            char_data = json.load(file)

        build = char_data["build"]
        wins = char_data["wins"]
        losses = char_data["losses"]
        forfeits = char_data["forfeits"]
        trait = char_data["trait"]
        total = wins + losses

        if trait == "cursed":
            msg.append(
                profile + "'s character name is: " + name
                + ", and they are a level: " + str(char_data["level"])
                + " [color=pink]" + build + "[/color] build. "
                + "They are also [color=cyan]cursed[/color]"
            )
        else:
            msg.append(
                profile + "'s character name is: " + name
                + ", and they are a level: " + str(char_data["level"])
                + " [color=pink]" + build + "[/color] build."
            )

        try:
            ratio = int((wins / total) * 100)
            msg.append(
                name + "'s current win/loss score is: [color=pink]"
                + str(wins) + " wins[/color], and "
                + "[color=yellow]" + str(losses)
                + " losses[/color]. ([color=red]" + str(ratio)
                + "%[/color]) They have also [color=green]forfeited "
                + str(forfeits) + " times.[/color]"
            )
        except ZeroDivisionError:
            msg.append(
                "Either " + name
                + " has a 0% win/loss ratio, or 100%. It all depends "
                + "on how you justify a person that has never entered the arena yet."
            )

    except FileNotFoundError:
        msg.append(
            profile + " isn't a valid name for a character sheet. You are just typing "
            "in their [color=red]profile name.[/color] example: !who <profile name>"
        )

    return msg


def build_character_player_score_message(char_folder, profile_name):
    profile = profile_name.lower()
    character_path = Path(char_folder) / f"{profile}.json"

    if not character_path.is_file():
        return (
            "Either they don't have a character, or you fucked up typing. (type: !player <profile name>, "
            "[b]not[/b] character name. Example: !player their perfect doll"
        )

    with character_path.open("r", encoding="utf-8") as character_file:
        score = json.load(character_file)

    name = score["name"]
    wins = score["wins"]
    losses = score["losses"]
    forfeits = score["forfeits"]
    total = wins + losses

    try:
        ratio = int((wins / total) * 100)
        return (
            name + "'s current win/loss score is: [color=pink]" + str(wins) + " wins[/color], "
            "and [color=yellow]" + str(losses) + " losses[/color]. ([color=red]" + str(ratio) + "%[/color])"
            "They have also forfeited " + str(forfeits) + " times."
        )
    except ZeroDivisionError:
        return (
            "Either " + name + " has a 0% win/loss ratio, or 100%. It all depends "
            "on how you justify a person that has never entered the arena yet."
        )


def build_character_challenge_message(challenger_info, opponent_info, opponent_profile, challenger_profile):
    if opponent_profile == challenger_profile:
        return "You can't fight yourself. No one is that special."

    if len(challenger_info["hfeats taken"]) < challenger_info["total feats"]:
        return challenger_info["name"] + " has empty feat slots, and cannot fight yet"

    if len(opponent_info["hfeats taken"]) < opponent_info["total feats"]:
        return opponent_info["name"] + " has empty feat slots, and cannot fight yet"

    if challenger_info["trait"] == "cursed" or opponent_info["trait"] == "cursed":
        return (
            challenger_info["name"].title()
            + " is challenging "
            + opponent_info["name"].title()
            + " ("
            + opponent_profile.title()
            + ", "
            + "Type [color=pink]!accept[/color]) Please be aware that one of the opponents"
            + " is [color=cyan]cursed[/color], and no xp/renown will be awarded at end of match."
        )

    return (
        challenger_info["name"].title()
        + " is challenging "
        + opponent_info["name"].title()
        + " ("
        + opponent_profile.title()
        + ", "
        + "Type [color=pink]!accept[/color])"
    )