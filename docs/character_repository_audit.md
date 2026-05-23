## Completed Chapter 9 Work

The character repository foundation has been created and tested.

Implemented helpers:

- `normalize_character_name(character_name)`
- `get_character_path(character_name, characters_dir=CHARACTERS_DIR)`
- `character_exists(character_name, characters_dir=CHARACTERS_DIR)`
- `load_character(character_name, characters_dir=CHARACTERS_DIR)`
- `save_character(character_name, character_data, characters_dir=CHARACTERS_DIR)`

The following legacy functions now route character JSON access through `character_repository`:

### Read / Load Routes

- `message_4_who` in `original/onMSGUtils.py`
- `message_7_player` in `original/onMSGUtils.py`
- `message_10_challenge` in `original/onMSGUtils.py`
- `message_accept` in `original/onMSGAccept.py`

### Single-Character Write Routes

- `pri_6_build` in `original/onPRIUtils.py`
- `pri_4_add` in `original/onPRIUtils.py`
- `status_compile` in `original/onMSGUtils.py`
- `pri_viewchar` in `original/onPRIUtils.py`
- `pri_6_stats` in `original/onPRIUtils.py`
- `pri_7_respec` in `original/onPRIUtils.py`

Current test status:

- 108 tests passing

## Current Position

The safest read-only and simple single-character write paths have now been refactored.

The project should pause before moving into higher-risk mutable systems. The next targets involve either:

- creating or deleting character files
- updating `playerDatabase.json`
- modifying more complex inventory or economy data
- modifying multiple character files
- modifying combat result files

These should be handled with stricter tests before any production code changes.

## Remaining Refactor Targets

### Medium Risk

These are probably the next reasonable candidates, but they need dedicated tests first:

- `message_5_name` in `original/onMSGUtils.py`
  - Creates a new character file.
  - Updates `playerDatabase.json`.
  - Depends on `levelchart.json`.

- `message_7_erase` in `original/onMSGUtils.py`
  - Deletes a character file.
  - Updates `playerDatabase.json`.

### High Risk

These should wait until creation/deletion and database helpers are better isolated:

- potion buy/use/give/sell commands
- armor buy/equip/unequip/sell commands
- renown transfer commands
- any function that modifies two character files

### Very High Risk

Avoid until later:

- `playerone_zero_current_hp.py`
- `playertwo_zero_current_hp.py`
- combat win/loss resolution
- level-up handling
- direct `botCommand.py` runtime integration

`botCommand.py` should still not be imported directly in pytest because of runtime dependencies.