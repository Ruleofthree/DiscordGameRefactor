import importlib
import json
import sys


def test_pri_6_trait_delegates_to_character_repository(monkeypatch, tmp_path):
    original_dir = tmp_path / "original"
    original_dir.mkdir()

    source_file = "original/onPRIUtils.py"
    target_file = original_dir / "onPRIUtils.py"
    target_file.write_text(open(source_file, encoding="utf-8").read(), encoding="utf-8")

    calls = {}

    def fake_select_character_trait(char_folder, character, message, trait_list, trait_dictionary, trait):
        calls["char_folder"] = char_folder
        calls["character"] = character
        calls["message"] = message
        calls["trait_list"] = trait_list
        calls["trait_dictionary"] = trait_dictionary
        calls["trait"] = trait
        return "delegated trait result"

    monkeypatch.syspath_prepend(str(tmp_path))
    module = importlib.import_module("original.onPRIUtils")

    monkeypatch.setattr(
        module,
        "select_character_trait",
        fake_select_character_trait,
    )

    monkeypatch.setattr(
        module,
        "refresh_character_combat_totals",
        lambda character, char_folder: None,
    )

    result = module.pri_6_trait(
        character="Tester",
        message="!traitpick brawler",
        traitList=["brawler"],
        traitDictionary=[{"brawler": {"bonus": [1, 2, 3, 4, 5]}}],
        trait="brawler",
    )

    assert result == "delegated trait result"
    assert calls["character"] == "Tester"
    assert calls["message"] == "!traitpick brawler"
    assert calls["trait_list"] == ["brawler"]
    assert calls["trait_dictionary"] == [{"brawler": {"bonus": [1, 2, 3, 4, 5]}}]
    assert calls["trait"] == "brawler"