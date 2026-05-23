import json
import pytest
from src.data_loader import (
    DATA_DIR,
    load_armor,
    load_data_file,
    load_feats,
    load_json_file,
    load_potions,
    load_traits,
)


def test_load_json_file_loads_valid_json(tmp_path):
    test_file = tmp_path / "sample.json"
    test_data = {"name": "test", "level": 1}

    test_file.write_text(json.dumps(test_data), encoding="utf-8")

    result = load_json_file(test_file)

    assert result == test_data


def test_load_data_file_loads_traits_json():
    result = load_data_file("traits.json")

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "regeneration" in result[0]


def test_load_data_file_loads_feats_json():
    result = load_data_file("feats.json")

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "power attack" in result[0]


def test_load_data_file_raises_file_not_found_for_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data_file("missing_file.json")


def test_data_dir_points_to_existing_data_folder():
    assert DATA_DIR.exists()
    assert DATA_DIR.is_dir()


def test_load_feats_loads_feats_json():
    result = load_feats()

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "power attack" in result[0]


def test_load_traits_loads_traits_json():
    result = load_traits()

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "regeneration" in result[0]


def test_load_potions_loads_potions_json():
    result = load_potions()

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "common" in result[0]


def test_load_armor_loads_armor_json():
    result = load_armor()

    assert isinstance(result, list)
    assert isinstance(result[0], dict)
    assert "armorlist" in result[0]