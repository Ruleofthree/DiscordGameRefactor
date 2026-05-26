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

from onPRIUtils import pri_10_sellarmor


def test_pri_10_sellarmor_writes_character_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    characters_dir = tmp_path / "characters"
    characters_dir.mkdir()

    character_data = {
        "name": "Test Character",
        "renown": 100,
        "equip": "",
        "armor": {
            "armor1": ["str1", "ac1", 2500],
            "armor2": "n/a",
            "armor3": "n/a",
        },
    }

    character_file = characters_dir / "tester.json"
    character_file.write_text(
        json.dumps(character_data),
        encoding="utf-8",
    )

    msg = pri_10_sellarmor(
        "tester",
        "armor1",
        str(characters_dir) + os.sep,
    )

    updated_character = json.loads(character_file.read_text(encoding="utf-8"))

    assert updated_character["renown"] == 1350
    assert updated_character["armor"]["armor1"] == "n/a"
    assert msg == "tester sold some armor for [color=yellow] 1250 renown[/color]"


