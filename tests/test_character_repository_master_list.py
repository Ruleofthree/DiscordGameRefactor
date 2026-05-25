from src.character_repository import build_active_character_master_list


def test_build_active_character_master_list_filters_out_bot_identity():
    users = [
        {"identity": "Alice"},
        {"identity": "Unspoiled Desire"},
        {"identity": "Bob"},
    ]

    master_list = build_active_character_master_list(users)

    assert master_list == ["Alice", "Bob"]


def test_build_active_character_master_list_preserves_user_order():
    users = [
        {"identity": "Charlie"},
        {"identity": "Alice"},
        {"identity": "Bob"},
    ]

    master_list = build_active_character_master_list(users)

    assert master_list == ["Charlie", "Alice", "Bob"]


def test_build_active_character_master_list_returns_empty_list_when_only_bot_is_present():
    users = [
        {"identity": "Unspoiled Desire"},
    ]

    master_list = build_active_character_master_list(users)

    assert master_list == []


def test_build_active_character_master_list_returns_empty_list_for_empty_users():
    master_list = build_active_character_master_list([])

    assert master_list == []