import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

import onPRIUtils


def test_pri_potionshop_loads_potion_data_and_returns_shop_display(monkeypatch):
    potion_data = [{"shoplist": ["hp5"]}]

    monkeypatch.setattr(
        onPRIUtils,
        "get_potion_dictionary",
        lambda: potion_data,
    )
    monkeypatch.setattr(
        onPRIUtils,
        "build_potion_shop_display",
        lambda loaded_data: "hp5: [color=red]1[/color] [color=yellow](150 renown)[/color]",
    )

    result = onPRIUtils.pri_potionshop()

    assert result == "hp5: [color=red]1[/color] [color=yellow](150 renown)[/color]"