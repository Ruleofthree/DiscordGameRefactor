import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onPRIUtils import pri_9_buyarmor


def test_pri_9_buyarmor_writes_character_and_armor_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    armor_data = [
        {
            "cat1": {
                "common": {"str1": [500, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat2": {
                "common": {"ac1": [2000, 1]},
                "uncommon": {},
                "rare": {},
            },
            "cat3": {
                "common": {},
                "uncommon": {},
                "rare": {},
            },
            "armorlist": {
                "armor1": ["str1", "ac1"],
            },
        }
    ]

    character_data = {
        "name": "Test Character",
        "renown": 3000,
        "armor": {
            "armor1": "n/a",
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    armor_file = tmp_path / "armor.json"
    armor_file.write_text(
        json.dumps(armor_data),
        encoding="utf-8",
    )

    character_file = characters_dir / "tester.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "onPRIUtils.get_armor_dictionary",
        lambda: armor_data,
    )

    msg = pri_9_buyarmor(
        "tester",
        "armor1",
        str(characters_dir) + os.sep,
    )

    updated_character = json.loads(character_file.read_text(encoding="utf-8"))
    updated_armor = json.loads(armor_file.read_text(encoding="utf-8"))

    assert updated_character["renown"] == 500
    assert updated_character["armor"]["armor1"] == ["str1", "ac1", 2500]
    assert updated_armor[0]["armorlist"]["armor1"] == "sold"
    assert msg == "Test Character has purchased an armor of [color=red]str1, ac1[/color]."