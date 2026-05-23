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