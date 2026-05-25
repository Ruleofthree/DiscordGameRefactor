# Character Repository Audit

## Purpose

This audit tracks the refactor of character-related logic from the legacy bot files into repository-backed functions under `src/`.

The goal is to preserve legacy behavior while gradually moving file access, character lifecycle operations, and reusable data handling out of large runtime command files.

The guiding rules for this refactor are:

- Write tests before changing behavior.
- Do not import `original/botCommand.py` in pytest.
- Use temporary test directories and temporary JSON files.
- Do not touch live character data.
- Keep bot runtime behavior unchanged unless deliberately refactoring a specific command.
- Avoid broad changes to combat, potions, armor, renown transfer, and unrelated systems while working on character lifecycle code.

---

## Current Test Status

Current full pytest result:

- `258 passed`

This includes:

- Data loader tests
- Feat repository tests
- Trait repository tests
- Armor repository tests
- Potion repository tests
- Character repository tests
- Character creation and deletion tests
- Character build, stat, trait, feat, ability-point, level-listing, and view-calculation tests
- Character challenge message and challenge acceptance tests
- Character renown transfer tests
- Character leaderboard message tests
- Character status compile boundary and passive status timer tests
- Legacy wrapper tests for selected `onMSGUtils.py`, `onPRIUtils.py`, and `onMSGAccept.py` command functions

---

## Why botCommand.py Is Avoided in Tests

`original/botCommand.py` is still a runtime-heavy legacy file.

It imports bot framework dependencies and attempts to interact with runtime files and credentials that are not appropriate for isolated pytest testing.

For that reason:

- `botCommand.py` is not imported directly in pytest.
- Refactored command logic should be moved into smaller testable functions.
- Tests should target repository modules or helper modules such as `original/onMSGUtils.py`, `original/onPRIUtils.py`, and `original/onMSGAccept.py`.
- `botCommand.py` should remain a thin caller where possible until it can be safely reduced later.

---

## Completed Repository Foundations

### Data Loader

A tested data-loading layer was created first so repository modules could rely on shared JSON-loading behavior.

Created:

- `src/data_loader.py`

Purpose:

- Reduce repeated raw `open(... json.load(...))` patterns.
- Give repository modules a consistent file-loading foundation.
- Keep tests isolated and predictable.

Status:

- Complete.

---

## Feat Repository Refactor

### Completed Work

Created:

- `src/feat_repository.py`

The feat repository supports loading feat data and returning the legacy shape expected by older command functions.

Legacy behavior preserved:

- Some legacy code expects both the feat dictionary and a list of feat names.
- The repository keeps that structure available so existing behavior does not change.

Tests added:

- Repository tests for feat loading.
- Legacy behavior tests for the old expected feat dictionary/list shape.

Status:

- Complete for read-only feat loading.

Not yet refactored:

- Combat feat behavior
- Active feat resolution
- Runtime fight calculations
- `feat_methods.py` internal JSON reads

These should be handled in a later combat or feat-behavior chapter.

---

## Trait Repository Refactor

### Completed Work

Created:

- `src/trait_repository.py`

The trait repository supports loading trait data and exposing the legacy shape needed by existing code.

Completed:

- Repository tests for trait loading.
- Trait data loading was separated from trait selection behavior.
- `botCommand.py` remained excluded from pytest imports.

Status:

- Complete for read-only trait loading.

Trait selection itself was later handled through the character repository work.

---

## Armor Repository Refactor

### Completed Work

Created:

- `src/armor_repository.py`

The armor repository supports loading armor data from JSON and preserving the expected legacy shop/list structure.

Completed:

- Repository tests for armor loading.
- Search was performed for armor shop usage.
- Legacy runtime write behavior was left untouched.
- No combat, equipment, or armor purchasing logic was changed.

Status:

- Complete for read-only armor data loading.

Not yet refactored:

- Buying armor
- Selling armor
- Equipping armor
- Unequipping armor
- Armor bonus recalculation
- Armor write behavior

Those should be handled in a later armor lifecycle chapter.

---

## Potion Repository Refactor

### Completed Work

Created:

- `src/potion_repository.py`

The potion repository supports loading potion data from JSON and preserving legacy potion shop/list behavior.

Completed:

- Repository tests for potion loading.
- Read-only potion loading was isolated from runtime command logic.
- Selected potion-related helper behavior was reviewed.
- Broad potion runtime behavior was not mixed into unrelated chapters.

Status:

- Complete for read-only potion data loading.

Not yet refactored:

- Buying potions
- Selling potions
- Giving potions
- Using potions
- Potion effects in combat
- Temporary potion modifiers
- Permanent potion progression

These should remain separate from character repository work.

---

## Legacy Read-Only Audit

### Completed Work

A read-only audit chapter was used to identify remaining legacy JSON-loading patterns.

Reviewed areas included:

- Feats
- Traits
- Armor
- Potions
- Legacy helper functions
- Places where direct JSON reads still exist

Purpose:

- Separate read-only data access from write-heavy runtime behavior.
- Avoid mixing repository cleanup with combat, economy, or character mutation systems.
- Identify medium-risk areas for later chapters.

Status:

- Complete as a broad audit.

---

## Character Repository Foundation

### Completed Work

Created and expanded:

- `src/character_repository.py`

The character repository now supports basic character file operations.

Completed helpers include:

- `normalize_character_name(character_name)`
- `get_character_path(character_name, characters_dir=CHARACTERS_DIR)`
- `character_exists(character_name, characters_dir=CHARACTERS_DIR)`
- `load_character(character_name, characters_dir=CHARACTERS_DIR)`
- `save_character(character_name, character_data, characters_dir=CHARACTERS_DIR)`

The repository uses caller-provided character folders during tests, allowing pytest to use temporary directories instead of live character data.

Status:

- Complete.

---

## Character Deletion Refactor

### Completed Work

Character deletion was moved into the repository layer.

Created:

- `delete_character()` in `src.character_repository`

Legacy wrapper:

- `original/onMSGUtils.py` `message_7_erase()` now delegates to `delete_character()`.

Behavior preserved:

- Character deletion still removes the character JSON file.
- Character deletion still removes the player database entry.
- Missing-character behavior remains compatible with legacy expectations.

Tests added:

- Repository deletion tests
- Legacy wrapper tests for erase behavior

Status:

- Complete.

---

## Character Creation Refactor

### Completed Work

Character creation was extracted from legacy command logic into the repository layer.

Created:

- `create_character()` in `src.character_repository`

Legacy wrapper:

- `original/onMSGUtils.py` `message_5_name()` delegates to `create_character()`.

Behavior preserved:

- Character sheet creation
- `levelchart.json` dependency
- `playerDatabase.json` update
- Existing-character rejection
- Legacy default character fields
- Legacy success and instruction messages

Important default fields preserved include:

- `name`
- `level`
- `build`
- `trait`
- `hp`
- `total feats`
- `base damage`
- `hit`
- `damage`
- `ac`
- `currentxp`
- `nextlevel`
- `strength`
- `dexterity`
- `constitution`
- `remaining feats`
- `ap`
- `apboost`
- `regeneration`
- `feats taken`
- `hfeats taken`
- `armor`
- `equip`
- `reset`
- `wins`
- `losses`
- `forfeits`
- `renown`
- `initiative`
- potion fields
- armor bonus fields
- trait bonus fields
- `status`
- `statuscounter`
- `fight`

Tests added:

- Repository tests for character creation
- Legacy wrapper tests for `message_5_name()`

Status:

- Complete.

---

## Character Build Command Extraction

### Completed Work

The private `!build` command behavior was extracted from `original/onPRIUtils.py`.

Created:

- `select_character_build()` in `src.character_repository`

Legacy wrapper:

- `pri_6_build()` now delegates to `select_character_build()`.

Behavior preserved:

- Strength, Dexterity, and Constitution builds are still recorded on the character sheet.
- Strength builds still receive `focus` automatically at the legacy low-level threshold.
- Existing builds are not overwritten.
- Legacy success and rejection messages are preserved.

Tests:

- `tests/test_character_repository_build.py`
- `tests/test_legacy_onpriutils_build.py`

Status:

- Complete.

---

## Character Stat Assignment Extraction

### Completed Work

The private `!stats` command behavior was extracted from `original/onPRIUtils.py`.

Created:

- `assign_character_stats()` in `src.character_repository`

Legacy wrapper:

- `pri_6_stats()` now delegates to `assign_character_stats()`.

Behavior preserved:

- Stat totals must match available ability points.
- Stat caps by level are preserved.
- Negative stats are rejected.
- Missing build selection is rejected.
- Strength, Dexterity, and Constitution build math is preserved.
- Character JSON is updated through temporary test-safe paths during testing.

Tests:

- `tests/test_character_repository_stats.py`
- `tests/test_legacy_onpriutils_stats.py`

Status:

- Complete.

---

## Character Respec Extraction

### Completed Work

The private `!respec` command behavior was tested and refactored.

Behavior covered:

- Free reset usage when reset points remain.
- Renown-cost reset when reset points are exhausted.
- Rejection when neither reset points nor sufficient renown are available.
- Legacy field resets for build, stats, traits, feats, derived bonuses, and related character fields.

Tests:

- `tests/test_legacy_onpriutils_respec.py`

Status:

- Complete for current tested behavior.

---

## Character Trait Selection Extraction

### Completed Work

The private `!traitpick` command behavior was extracted from `original/onPRIUtils.py`.

Created:

- `select_character_trait()` in `src.character_repository`

Legacy wrapper:

- `pri_6_trait()` now delegates to `select_character_trait()`.

Behavior preserved:

- Trait selection uses the legacy trait dictionary/list structure.
- Trait bonuses are applied according to character level.
- Invalid traits and already-selected traits are rejected.
- Character JSON is updated through repository-backed logic.

Tests:

- `tests/test_character_repository_traits.py`

Status:

- Complete for current tested behavior.

---

## Character Feat Selection Extraction

### Completed Work

The private `!featpick` command behavior was extracted from `original/onPRIUtils.py`.

Created:

- `select_character_feat()` in `src.character_repository`

Legacy wrapper:

- `pri_10_feat_pick()` now delegates to `select_character_feat()`.

Behavior preserved:

- Feat list validation
- Build restrictions
- Level restrictions
- Prerequisite checks
- Remaining feat slot handling
- Hidden feat tracking
- Legacy automatic and restricted feat behavior

Tests:

- `tests/test_character_repository_feats.py`

Status:

- Complete for current tested behavior.

---

## Character View Calculation Extraction

### Completed Work

The calculation and display-preparation portions of `pri_viewchar()` were extracted into `src.character_repository`.

Created:

- `calculate_character_view_totals()`
- `format_character_view_armor_inventory()`
- `format_character_view_potion_inventory()`
- `build_character_view_context()`
- `apply_character_view_totals()`

Legacy wrapper:

- `pri_viewchar()` still owns the final F-list display string and save operation.
- Calculation and context-building logic now lives in repository helpers.

Behavior preserved:

- Strength, Dexterity, and Constitution build math
- HP, AC, hit, damage, DR, regeneration, blur, and initiative calculations
- Legacy armor inventory formatting behavior
- Legacy potion inventory formatting behavior
- Legacy armor mutation behavior during view formatting

Tests:

- `tests/test_character_repository_view_totals.py`
- `tests/test_character_repository_view_context.py`
- `tests/test_character_repository_apply_view_totals.py`
- `tests/test_legacy_onpriutils_viewchar.py`

Status:

- Complete for calculation/context extraction.
- Final F-list display formatting remains in `pri_viewchar()`.

---

## Ability Point Add Extraction

### Completed Work

The private `!add` command behavior was extracted from `original/onPRIUtils.py`.

Created:

- `add_ability_point()` in `src.character_repository`

Legacy wrapper:

- `pri_4_add()` now delegates to `add_ability_point()`.

Behavior preserved:

- Accepts `strength` and `str`.
- Accepts `dexterity` and `dex`.
- Accepts `constitution` and `con`.
- Rejects invalid ability names.
- Requires `apboost` to be available.
- Adds one point to the selected ability.
- Sets `apboost` to `False`.
- Preserves the legacy response messages.

Tests:

- `tests/test_character_repository_add_ability_point.py`
- `tests/test_legacy_onpriutils_add.py`

Status:

- Complete.

---

## Character Level Listing Extraction

### Completed Work

The private `!wholevel` behavior was extracted from `original/onPRIUtils.py`.

Created:

- `list_characters_by_level()` in `src.character_repository`

Legacy wrapper:

- `pri_9_wholevel()` now delegates the lookup work to `list_characters_by_level()`.

Behavior preserved:

- Reads `playerDatabase.json`.
- Loads each listed character file.
- Filters profiles by exact character level.
- Preserves player database order.
- Keeps final F-list message formatting in `pri_9_wholevel()`.

Tests:

- `tests/test_legacy_onpriutils_wholevel.py`
- `tests/test_character_repository_wholevel.py`

Status:

- Complete.

---

## Character Who Lookup Extraction

### Completed Work

The public `!who <profile name>` command behavior was extracted from `original/onMSGUtils.py`.

Created:

- `build_character_who_messages()` in `src.character_repository`

Legacy wrapper:

- `message_4_who()` now delegates profile lookup and message construction to `build_character_who_messages()`.

Behavior preserved:

- Command still only works in the Unspoiled Desire OOC room.
- Profile names are still read from `playerDatabase.json`.
- Character sheets are still loaded by profile name.
- Character name, level, build, cursed status, wins, losses, forfeits, and win/loss ratio are still displayed.
- Zero-fight characters still use the original ZeroDivisionError fallback message.
- Missing character sheets still use the original invalid-profile message.
- Legacy output strings were preserved.

Tests:

- `tests/test_character_repository_who.py`
- `tests/test_legacy_onmsgutils_who.py`

Status:

- Complete.

---

## Character Player Score Extraction

### Completed Work

The deprecated public `!player <profile name>` command behavior was extracted from `original/onMSGUtils.py`.

Created:

- `build_character_player_score_message()` in `src.character_repository`

Legacy wrapper:

- `message_7_player()` now delegates player score message construction to `build_character_player_score_message()`.

Behavior preserved:

- Command still only works in the Unspoiled Desire OOC room.
- Profile names are still read from the `!player` command text.
- Character sheets are still loaded by profile name.
- Existing character profiles still display wins, losses, forfeits, and win/loss ratio.
- Zero-fight characters still use the original ZeroDivisionError fallback message.
- Missing character sheets still use the original missing-character message.
- Legacy output strings were preserved, including spacing and punctuation.

Tests:

- `tests/test_character_repository_player_score.py`
- `tests/test_legacy_onmsgutils_player.py`

Status:

- Complete.

---

## Character Leaderboard Extraction

### Completed Work

The public `!leaderboard` command behavior was extracted from `original/onMSGUtils.py`.

Created:

- `build_character_leaderboard_messages()` in `src.character_repository`

Legacy wrapper:

- `message_12_leaderboard()` now delegates leaderboard message construction to `build_character_leaderboard_messages()`.

Behavior preserved:

- Command still only works in the Unspoiled Desire OOC room.
- `!leaderboard win` still sorts by wins.
- `!leaderboard loss` still sorts by losses.
- `!leaderboard percent` still sorts by win percentage.
- Unknown leaderboard categories still default to wins.
- Zero-fight characters still use `0` percent.
- Player database order is still used before sorting.
- The legacy top-five output shape is preserved.
- Legacy output strings were preserved, including spacing, color tags, and percentage formatting.

Tests:

- `tests/test_character_repository_leaderboard.py`
- `tests/test_legacy_onmsgutils_leaderboard.py`

Status:

- Complete.

## Character Renown Transfer Extraction

### Completed Work

The public `!giverenown <amount> <profile name>` command behavior was extracted from `original/onMSGUtils.py`.

Created:

- `transfer_character_renown()` in `src.character_repository`

Legacy wrapper:

- `message_11_giverenown()` now delegates renown transfer behavior to `transfer_character_renown()`.

Behavior preserved:

- Command still only works in the Unspoiled Desire OOC room.
- Missing gifter character files still use the original missing-character message.
- Missing recipient character files still use the original missing-character message.
- Insufficient renown still rejects the transfer with the original message.
- Successful transfers still subtract renown from the gifter.
- Successful transfers still add renown to the recipient.
- Successful transfers still use the original success message shape.
- Wrong-channel behavior is preserved as `None`.

Tests:

- `tests/test_character_repository_renown_transfer.py`
- `tests/test_legacy_onmsgutils_giverenown.py`

Status:

- Complete.

## Character Status Compile Boundary

### Completed Work

The status parsing and character status mutation boundary from `original/onMSGUtils.py` was tested and moved behind a repository helper.

Created:

- `update_character_status_from_status_message()` in `src.character_repository`

Legacy wrapper:

- `status_compile()` now delegates status parsing and status-field mutation to `update_character_status_from_status_message()`.

Behavior preserved:

- Characters in the active master list can have their `status` field updated from the legacy OOC room status text.
- Characters not in the master list are ignored.
- Status messages without the expected legacy OOC room marker continue to leave the existing status unchanged.
- Missing character files continue to be swallowed without raising an error.
- Malformed status text continues to be swallowed without raising an error.
- Character status updates do not touch `statuscounter` or `renown`.
- Character JSON access remains testable through temporary character directories.

Tests:

- `tests/test_character_repository_status.py`
- `tests/test_legacy_onmsgutils_status_compile.py`

Status:

- Complete for current status compile boundary behavior.

## Character Passive Status Timer Boundary

### Completed Work

The passive status timer character-file mutation behavior from `botCommand.py` was extracted into the character repository layer.

Created:

- `apply_passive_status_timer_tick()` in `src.character_repository`

Legacy wrapper:

- `statusTimer()` in `original/botCommand.py` now delegates character statuscounter and passive renown mutation to `apply_passive_status_timer_tick()`.

Behavior preserved:

- Characters in the active master list are checked for an existing character sheet.
- Missing character files are skipped.
- When the timer counter is `24`, character `statuscounter` is reset to `0`.
- Characters whose `status` is the Unspoiled Desire OOC room and whose `statuscounter` is `10` or lower still receive `10` renown.
- Characters receiving passive renown still have `statuscounter` incremented by `1`.
- The timer counter still increments while below `25`.
- The timer counter still wraps back to `0` after reaching `25`.
- Runtime printing remains in `botCommand.py`.
- Sending `!status` to `Unspoiled Desire` remains in `botCommand.py`.
- `botCommand.py` is still not imported directly in pytest.

Tests:

- `tests/test_character_repository_status.py`

Status:

- Complete for passive status timer character-file mutation behavior.

## Character Challenge Message Extraction

### Completed Work

The public `!challenge <profile name>` message-construction behavior was extracted from `original/onMSGUtils.py`.

Created:

- `build_character_challenge_message()` in `src.character_repository`

Legacy wrapper:

- `message_10_challenge()` now delegates challenge message construction to `build_character_challenge_message()`.

Behavior preserved:

- Valid challenges still produce the legacy challenge message.
- Cursed-opponent warnings are still included when either character has the `cursed` trait.
- Self-challenges are still rejected with the legacy message.
- Challengers with empty feat slots are still rejected.
- Opponents with empty feat slots are still rejected.
- Legacy return shapes and challenge state values are preserved.
- Legacy wrong-channel, active-game, and pending-game error behavior is preserved.

Tests:

- `tests/test_character_repository_challenge.py`
- `tests/test_legacy_onmsgutils_challenge.py`

Status:

- Complete.

---

## Character Challenge Acceptance Boundary

### Completed Work

The public `!accept` challenge acceptance boundary was tested and partially extracted from `original/onMSGAccept.py`.

Created:

- `build_challenge_accept_initiative_result()` in `src.character_repository`
- `build_challenge_acceptance_result()` in `src.character_repository`

Legacy wrapper:

- `message_accept()` in `original/onMSGAccept.py` now delegates challenge acceptance state construction and initiative message construction to repository helpers.

Behavior preserved:

- Successful challenge acceptance still starts the fight state.
- The accepting player is still loaded from the character folder.
- Player two is still set from the accepting character profile.
- Initiative rolls are still generated inside `message_accept()`.
- Initiative totals are still calculated using each character's initiative modifier.
- Player one still wins the final tie-breaker when the coin flip result is `1`.
- Wrong accepting characters are still rejected with the legacy message.
- Attempts to accept when no challenge is pending are rejected.
- Attempts to accept outside the arena channel are rejected.
- Legacy return tuple shape is preserved.
- Wrong accepting characters still preserve the legacy rejection message through repository-backed acceptance handling.
- Missing pending-opponent values still preserve the legacy expired-challenge message.
- Legacy timer flags, update flags, player-two assignment, new-game state, and token return values remain compatible with the existing caller.

Boundary stabilization:

- `message_accept()` now initializes its return-state values before channel and game-state branching.
- This prevents invalid acceptance paths from failing with uninitialized local variable errors.
- The misspelled `new_oppenent` return variable is preserved for compatibility with existing callers.

Tests:

- `tests/test_character_repository_acceptance.py`
- `tests/test_legacy_onmsgaccept.py`

Status:

- Complete for challenge acceptance boundary, acceptance state construction, and initiative result extraction.

---

## Current Position

The safest read-only and simple character repository paths have now been refactored and tested.

Completed character-related areas include:

- Character file path helpers
- Character existence checks
- Character loading
- Character saving
- Character creation
- Character deletion
- Build selection
- Stat assignment
- Respec behavior
- Trait selection
- Feat selection
- Ability-point adding
- Character level listing
- Character who/profile lookup
- Character player score lookup
- Character leaderboard message construction
- Character renown transfer behavior
- Character challenge message construction
- Character challenge acceptance boundary behavior
- Character challenge acceptance state construction
- Character challenge acceptance initiative message construction and token selection
- Character view calculations and context preparation
- Character status compile boundary behavior

`botCommand.py` is still not imported directly in pytest because of runtime dependencies.

`original/onPRIUtils.py` still contains the final F-list display formatter for `pri_viewchar()`, along with the remaining potion, armor, shop, and equipment functions.

`original/onMSGUtils.py` still contains combat-facing helpers and economy-facing helpers that should not be mixed into general character lookup cleanup.

---

## Remaining Refactor Targets

### Medium Risk

These are reasonable future targets, but they need dedicated tests first:

- Further `message_accept` cleanup in `original/onMSGAccept.py`
  - Random initiative roll generation still happens inside the legacy wrapper.
  - Coin-flip detection still performs a lightweight character load in the legacy wrapper.
  - Timer handoff behavior remains owned by `botCommand.py`.
  - Full combat-start state integration remains in the legacy runtime path.
  - Any further extraction should be handled carefully with additional legacy tests.

- Further status parsing cleanup
  - The current boundary is tested and delegated.
  - Broad exception behavior is still preserved intentionally.
  - Any future cleanup should first decide whether malformed status strings should continue to no-op or be handled explicitly.

### High Risk

These should wait for dedicated inventory/economy chapters:

- `pri_10_stockpotion`
- `pri_10_buypotion`
- `pri_11_sellpotion`
- `pri_10_usepotion`
- `pri_11_givepotion`
- `pri_11_stockarmor`
- `pri_10_armorshop`
- `pri_9_buyarmor`
- `pri_10_sellarmor`
- `pri_10_namearmor`
- `pri_6_equip`
- `pri_8_unequip`

These functions touch inventory, shop data, equipment state, temporary modifiers, permanent modifiers, or combat-adjacent character state.

### Very High Risk

Avoid until later:

- `message_8_usefeat`
- `message_5_pass`
- `playerone_zero_current_hp.py`
- `playertwo_zero_current_hp.py`
- `Roll_true_strike.py`
- `Roll_not_strike.py`
- `feat_methods.py`
- combat win/loss resolution
- XP and renown payout logic
- level-up handling
- combat feat execution
- rolling resolution
- direct `botCommand.py` runtime integration