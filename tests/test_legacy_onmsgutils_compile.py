import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_DIR = PROJECT_ROOT / "original"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(ORIGINAL_DIR) not in sys.path:
    sys.path.insert(0, str(ORIGINAL_DIR))

from onMSGUtils import message_8_compile


def test_message_8_compile_filters_out_bot_identity():
    users = [
        {"identity": "Alice"},
        {"identity": "Unspoiled Desire"},
        {"identity": "Bob"},
    ]

    master_list = message_8_compile(users)

    assert master_list == ["Alice", "Bob"]


def test_message_8_compile_preserves_user_order():
    users = [
        {"identity": "Charlie"},
        {"identity": "Alice"},
        {"identity": "Bob"},
    ]

    master_list = message_8_compile(users)

    assert master_list == ["Charlie", "Alice", "Bob"]


def test_message_8_compile_returns_empty_list_when_only_bot_is_present():
    users = [
        {"identity": "Unspoiled Desire"},
    ]

    master_list = message_8_compile(users)

    assert master_list == []