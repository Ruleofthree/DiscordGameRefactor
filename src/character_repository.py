import json
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