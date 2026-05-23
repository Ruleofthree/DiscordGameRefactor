import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def load_json_file(path: str | Path) -> Any:
    """
    Load and return JSON data from a file.

    Accepts either:
    - a full path
    - a relative path
    - a string path
    """
    json_path = Path(path)

    with json_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_data_file(filename: str) -> Any:
    """
    Load a JSON from the project's data/ directory.
    """
    return load_json_file(DATA_DIR / filename)


def load_feats() -> Any:
    """
    Load feats.json from the data directory.
    """
    return load_data_file("feats.json")


def load_traits() -> Any:
    """
    Load traits.json from the data directory.
    """
    return load_data_file("traits.json")


def load_potions() -> Any:
    """
    Load potions.json from the data directory.
    """
    return load_data_file("potions.json")


def load_armor() -> Any:
    """
    Load armor.json from the data directory.
    """
    return load_data_file("armor.json")