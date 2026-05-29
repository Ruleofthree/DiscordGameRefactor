# Inventory and Economy Audit

## Purpose

This audit tracks inventory, economy, potion, armor, shop, and equipment refactor work after the character repository cleanup pass.

The goal is to preserve legacy behavior while gradually moving deterministic inventory and economy logic out of large
legacy command functions and into repository-backed helpers under `src/`.

The guiding rules for this refactor are:

* Write tests before changing behavior.
* Do not import `original/botCommand.py` in pytest.
* Use temporary test directories and temporary JSON files.
* Do not touch live character data.
* Preserve legacy behavior exactly unless a behavior change is deliberately chosen and tested.
* Keep file loading and saving in legacy wrappers unless a specific repository boundary is being targeted.
* Do not mix economy cleanup with combat, rolling, win/loss resolution, XP payout, renown payout, level-up handling,
potion lifecycle behavior, or equipment lifecycle behavior.

---

## Current Test Status

Current full pytest result:

* `416 passed`

This test result includes:

* Potion repository tests
* Armor repository tests
* Legacy wrapper tests for selected `onPRIUtils.py` inventory and economy functions
* Existing character repository, feat repository, trait repository, data loader, and legacy command tests

If the local full-suite pytest result changes, update only this section and any new completed extraction section being
added at that time.

---

## Current Position

The character repository cleanup pass is complete.

The inventory and economy pass has completed several smaller, testable extraction targets. The completed work now
covers read-only display behavior, shop restocking behavior, single-character potion economy behavior, potion transfer
behavior, potion use lifecycle behavior, potion use cleanup review, armor purchase behavior, armor sale behavior,
armor equipment lifecycle boundary behavior, and armor equipment lifecycle extraction.

The character-summary display boundary review also completed the focused `pri_viewchar()` display update. Character
view context construction, total calculation, and total write-back orchestration are repository-backed. The legacy
wrapper still owns character existence checking and private command return behavior.

Completed inventory/economy areas include:

* Read-only armor shop display
* Single-character potion sale
* Potion shop restock
* Potion purchase
* Potion transfer
* Potion use lifecycle extraction
* Potion use cleanup review
* Create potion boundary extraction
* Shop list loader boundary extraction
* Armor shop restock
* Armor purchase
* Armor sale
* Armor equipment lifecycle boundary audit
* Armor equipment lifecycle extraction

Repository-backed helpers now exist for:

* Building armor shop display text
* Selling potions
* Restocking the potion shop
* Buying potions
* Giving potions between characters
* Using potions
* Applying permanent stat potion progression
* Restocking the armor shop
* Buying armor
* Selling armor
* Renaming armor
* Equipping armor
* Unequipping armor
* Creating moderator-granted potions
* Loading potion shop list buckets
* Loading armor shop list buckets

Remaining targets are higher risk because they may touch combat-adjacent state, broader command/runtime behavior,
or behavior that has not yet been isolated behind repository helpers.

---

## Completed Extractions

### Armor Shop Display Extraction

Completed helper functions:

* `calculate_armor_effect_price()` in `src.armor_repository`
* `calculate_armor_item_price()` in `src.armor_repository`
* `build_armor_shop_display()` in `src.armor_repository`

Legacy wrapper:

* `pri_10_armorshop()` now delegates armor shop display construction to `build_armor_shop_display()`.

Behavior preserved:

* Single-attribute armor display is preserved.
* Two-attribute armor display is preserved.
* Three-attribute armor display is preserved.
* Sold armor still displays with `0` renown.
* Multiple armor entries still display in the same newline-separated format.
* Legacy color tags and output formatting are preserved.
* No character files are read or written.
* `armor.json` is not mutated by armor shop display.
* Buying, selling, naming, equipping, unequipping, and armor restocking behavior were not changed by this extraction.

Tests added or expanded:

* `tests/test_armor_repository.py`
* `tests/test_legacy_onpriutils_armorshop.py`

Status:

* Complete.

---

### Armor Shop Display Wrapper Boundary Extraction

The remaining `!armorshop` display boundary was reviewed after armor shop line formatting had already been moved behind `pri_10_armorshop()`.

A thin `pri_armorshop()` wrapper was added to `original/onPRIUtils.py`. The wrapper loads armor data through
`src.armor_repository.get_armor_dictionary()`, builds the armor display input list from `armor_dictionary[0]["armorlist"]`,
and returns the display body from `src.armor_repository.build_armor_shop_display()`.

`original/botCommand.py` now delegates armor shop body loading and construction to `pri_armorshop()`, while preserving
the legacy display header and `super().PRI(...)` delivery behavior in place.

This extraction does not change armor buying, armor selling, armor naming, armor equip, armor unequip, potion behavior,
combat behavior, rolling, XP payout, renown payout, or level-up handling.

Test coverage:

* `tests/test_legacy_onpriutils_armorshop.py` confirms `pri_armorshop()` loads armor data and returns the shop display body.
* Existing repository and legacy wrapper tests continue to cover armor shop line formatting.

---

### Shop List Loader Boundary Extraction

Raw shop list loading was removed from `original/botCommand.py`.

Thin wrappers were added to `original/onPRIUtils.py`:

* `pri_potion_shop_lists()`
* `pri_armor_shop_lists()`

`pri_potion_shop_lists()` delegates to `src.potion_repository.get_potion_shop_lists()`.

`pri_armor_shop_lists()` delegates to `src.armor_repository.get_armor_shop_lists()`.

`original/botCommand.py` now routes the remaining active potion and armor list-loading call sites through these wrappers
instead of using local `potionShop()` and `armorShop()` helper functions.

After a case-sensitive search confirmed that no active `potionShop()` or `armorShop()` call sites remained, the old
helper definitions were removed from `original/botCommand.py`.

Behavior preserved:

* `!stockpotion` still owns command routing and response behavior in `original/botCommand.py`.
* `!usepotion` still owns command routing and response behavior in `original/botCommand.py`.
* `!stockarmor` still owns command routing and response behavior in `original/botCommand.py`.
* Potion usage behavior was not changed.
* Potion effect behavior was not changed.
* Combat checks were not changed.
* Potion restock mutation logic was not changed.
* Armor restock mutation logic was not changed.
* Shop display wrappers `pri_potionshop()` and `pri_armorshop()` were not changed.
* Legacy formatting remains unchanged.

Tests added:

* `tests/test_legacy_onpriutils_shop_lists.py`

Verification:

* `python -m py_compile original/botCommand.py`
* `pytest tests/test_legacy_onpriutils_shop_lists.py`
* `pytest`

Status:

* Complete.

---

### Potion Shop Display Construction Extraction

`!potionshop` previously built the potion shop display body directly inside `original/botCommand.py` after opening `potions.json`.

The display construction has been extracted into `src.potion_repository.build_potion_shop_display()`.

The extracted helper preserves the legacy behavior:
- reads `potion_data[0]["shoplist"]`
- counts duplicate stocked potions with `Counter`
- preserves first-seen shop order from the stocked shop list
- resolves potion prices across `common`, `uncommon`, `rare`, `vrare`, and `relic`
- builds each display line in the legacy format:
  `<potion>: [color=red]<amount>[/color] [color=yellow](<price> renown)[/color]`

`original/botCommand.py` still owns command routing, `potions.json` loading, and private message delivery.
No buying, selling, transfer, use, stocking, armor, combat, XP, renown payout, or level-up behavior was changed.

Test coverage:
- `tests/test_potion_repository.py` verifies duplicate shop entries are counted correctly.
- `tests/test_potion_repository.py` verifies first-seen shop order is preserved.
- `tests/test_potion_repository.py` verifies potion prices are resolved from the expected rarity buckets.
- `tests/test_potion_repository.py` verifies an empty shop list returns an empty display body.

---

### Potion Shop Display Wrapper Boundary Extraction

The remaining `!potionshop` command boundary was reviewed after the shop display body construction was extracted.
The command still owns routing and private message delivery, while the potion repository owns deterministic shop display body construction.

A thin `pri_potionshop()` wrapper was added to `original/onPRIUtils.py`. The wrapper loads the potion dictionary
through the potion repository loader and returns the display body from `build_potion_shop_display()`.

`original/botCommand.py` now delegates potion shop body loading and construction to `pri_potionshop()`, while preserving
the legacy private message header and `super().PRI(...)` delivery behavior in place.

This extraction does not change potion buying, potion selling, potion transfer, potion use, shop stocking, armor
behavior, combat behavior, rolling, XP payout, renown payout, or level-up handling.

### Create Potion Boundary Extraction

* `!createpotion` still owns command routing, moderator gating, command input parsing, and notification sending in `original/botCommand.py`.
* `pri_createpotion()` loads potion data through `src.potion_repository.get_potion_dictionary()`.
* `pri_createpotion()` loads and saves the target character through the character repository helpers.
* `src.potion_repository.create_character_potion()` owns the rarity-bucket potion append decision.
* The extraction intentionally preserves legacy behavior for unknown potion names: unknown potion names do not append
  anything, but command-level success-style notifications remain unchanged.
* The extraction intentionally preserves the existing fragile command parser and missing-character handling behavior.
* Repository coverage now includes create-potion append behavior for common, uncommon, rare, very rare, relic, and unknown potion names.
* `original/botCommand.py` no longer opens `potions.json` directly inside the `!createpotion` command block.
* `original/botCommand.py` no longer directly writes the target character file inside the `!createpotion` command block.

Tests added or expanded:

* `tests/test_potion_repository.py`

Status:

* Complete.

---

### Potion Sale Extraction

Completed helper:

* `sell_character_potion()` in `src.potion_repository`

Legacy wrapper:

* `pri_11_sellpotion()` now delegates deterministic potion sale logic to `sell_character_potion()`.

Behavior preserved:

* Owned potions can still be sold for half their listed potion value.
* The seller's renown is still increased by the half-price value.
* The sold potion is still removed from the seller's potion inventory.
* Missing potions still return the legacy rejection message.
* Potions missing from potion data still return the legacy unknown-potion message.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* The legacy missing-character `UnboundLocalError` behavior is intentionally preserved and covered by test.
* Potion buying, potion use, potion transfer, potion restocking, armor behavior, combat behavior, XP payout, renown 
payout, and level-up handling were not changed by this extraction.

Tests added or expanded:

* `tests/test_potion_repository.py`
* `tests/test_legacy_onpriutils_sellpotion.py`

Status:

* Complete.

---

### Potion Transfer Extraction

Completed helper:

* `give_character_potion()` in `src.potion_repository`

Legacy wrapper:

* `pri_11_givepotion()` now delegates deterministic potion transfer-state mutation to `give_character_potion()` while
  keeping both character-file loads and both character-file writes in `original/onPRIUtils.py`.

Behavior preserved:

* Owned potions can still be transferred from the sender to the recipient.
* The transferred potion is still removed from the sender's potion inventory.
* The transferred potion is still appended to the recipient's potion inventory.
* The transferred potion name is still lowercased before transfer.
* Missing potions still return the legacy rejection message.
* Recipient inventory capacity still uses the legacy `len(potions) <= 3` rule.
* Recipients with no inventory space still receive the legacy inventory-space rejection message.
* Missing sender character files still return the legacy missing-sender message.
* Missing recipient character files still return the legacy missing-recipient message, including the existing `posiont` typo.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* Potion purchase, potion sale, potion use, potion restocking, armor behavior, combat behavior, rolling, XP payout,
  renown payout, and level-up handling were not changed by this extraction.

Tests added or expanded:

* `tests/test_potion_repository.py`
* `tests/test_legacy_onpriutils_givepotion.py`

Status:

* Complete.

### Potion Shop Restock Extraction

Completed helper:

* `stock_potion_shop()` in `src.potion_repository`

Legacy wrapper:

* `pri_10_stockpotion()` now delegates potion shop restock construction to `stock_potion_shop()` while keeping
`potions.json` file writing in `original/onPRIUtils.py`.

Behavior preserved:

* Potion shop restocking still replaces the existing `shoplist`.
* The shop still receives 20 potion entries.
* Legacy rarity thresholds are preserved:

  * `98-100` selects relic potions.
  * `90-97` selects very rare potions.
  * `77-89` selects rare potions.
  * `51-76` selects uncommon potions.
  * `1-50` selects common potions.
* Legacy random index selection behavior is preserved.
* The returned shop string is preserved.
* The returned restock message is preserved.
* Character files are not read or written.
* Potion buying, potion selling, potion use, potion transfer, armor behavior, combat behavior, XP payout, renown
payout, and level-up handling were not changed by this extraction.

Additional cleanup:

* A duplicate earlier `pri_10_stockpotion()` definition was removed from `original/onPRIUtils.py`.
* The remaining active `pri_10_stockpotion()` definition is the delegated wrapper.

Tests added or expanded:

* `tests/test_potion_repository.py`
* `tests/test_legacy_onpriutils_stockpotion.py`

Status:

* Complete.

---

### Potion Purchase Extraction

Completed helpers:

* `get_potion_price_from_data()` in `src.potion_repository`
* `buy_character_potion()` in `src.potion_repository`

Legacy wrapper:

* `pri_10_buypotion()` now delegates deterministic potion purchase-state mutation to `buy_character_potion()` while
keeping file loading and saving in `original/onPRIUtils.py`.

Behavior preserved:

* Available potions can still be purchased from the current potion shop.
* The buyer's renown is still reduced by the potion price.
* Purchased potions are still added to the buyer's potion inventory.
* Purchased potions are still removed from `potions.json` shop stock.
* Potions not currently for sale still return the legacy rejection message.
* Buyers without enough renown still receive the legacy insufficient-renown message.
* Buyers with full potion inventories still receive the legacy inventory-space message.
* The legacy misspelling `puchased` is intentionally preserved.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* `potions.json` loading and saving remain in `original/onPRIUtils.py`.
* Potion use, potion transfer, armor behavior, combat behavior, XP payout, renown payout, and level-up handling were
not changed by this extraction.

Tests added or expanded:

* `tests/test_potion_repository.py`
* `tests/test_legacy_onpriutils_buypotion.py`

Status:

* Complete.

---

### Potion Use Lifecycle Extraction

Completed helpers:

* `use_character_potion()` in `src.potion_repository`
* `_apply_permanent_stat_potion()` in `src.potion_repository`

Legacy wrapper:

* `pri_10_usepotion()` now delegates potion mutation and message behavior to `use_character_potion()` while keeping
  character-file loading and saving in `original/onPRIUtils.py`.

Behavior preserved:

* Permanent progression potions are preserved: `str1` through `str5`, `dex1` through `dex5`, and `con1` through `con5`
  still mutate `pstrength`, `pdexterity`, or `pconstitution` only when the existing progression field is exactly one tier lower.
* Permanent stat potion progression has been consolidated into `_apply_permanent_stat_potion()`.
* `_apply_permanent_stat_potion()` preserves the legacy success message, inventory removal behavior, and invalid-progression rejection message.
* `respec` still increments `reset`.
* `stimulant` still increments both `remaining feats` and `total feats`.
* Temporary next-match potions still set the matching potion bonus field and usually set `potioneffect`.
* Valid potion names are still checked through potion data lookup, not against character inventory before use. A valid
  potion name missing from inventory can still raise `ValueError` when removal is attempted.
* Unknown potion names still return `You do not have a potion of <potion>`.
* A character with an existing `potioneffect` still cannot drink another temporary potion.
* Permanent stat potions, `respec`, and `stimulant` are still handled before the temporary potion lock.
* Regeneration potions still set `potionregen` and `potioneffect`, but the successful branch still does not remove
  the potion from inventory.
* The regeneration eligibility condition still uses `traitdr == 0 or armordr == 0 or regeneration == 0`, which means
  the potion is blocked only when all three fields are nonzero.
* Existing messages, typos, spacing, field names, and questionable conditionals remain preserved.

Cleanup review result:

* The permanent stat potion progression block was the only safe cleanup boundary selected after extraction.
* Temporary potion behavior was intentionally left inside `use_character_potion()` because it contains fragile legacy
  behavior and combat-adjacent state setup.
* No behavior changes were made during the cleanup review.

Tests added or expanded:

* `tests/test_potion_repository.py`
* `tests/test_legacy_onpriutils_usepotion.py`

Status:

* Complete.

---

### Armor Shop Restock Extraction

Completed helper:

* `stock_armor_shop()` in `src.armor_repository`

Legacy wrapper:

* `pri_11_stockarmor()` now delegates armor shop restock construction to `stock_armor_shop()` while keeping 
`armor.json` file writing in `original/onPRIUtils.py`.

Behavior preserved:

* Armor shop restocking still creates 20 armor entries.
* Category-one armor attributes are still always selected.
* Category-two armor attributes are still only added when the legacy `rand` threshold allows it.
* Category-three armor attributes are still only added when the legacy `rand` threshold allows it.
* Legacy category rarity thresholds are preserved.
* Legacy random choice behavior is preserved.
* The returned message is preserved.
* Character files are not read or written.
* Armor buying, armor selling, armor naming, equipping, unequipping, potion use, potion transfer, combat behavior,
XP payout, renown payout, and level-up handling were not changed by this extraction.

Additional cleanup:

* The legacy wrapper no longer depends on an undefined module-level `armorDictionary`.
* `armor.json` writing remains in `original/onPRIUtils.py`.

Tests added or expanded:

* `tests/test_armor_repository.py`
* `tests/test_legacy_onpriutils_stockarmor.py`

Status:

* Complete.

---

### Armor Purchase Extraction

Completed helper:

* `buy_character_armor()` in `src.armor_repository`

Legacy wrapper:

* `pri_9_buyarmor()` now delegates deterministic armor purchase-state mutation to `buy_character_armor()` while keeping
file loading and saving in `original/onPRIUtils.py`.

Behavior preserved:

* Available armor can still be purchased from the current armor shop.
* The buyer's renown is still reduced by the calculated armor price.
* Purchased armor is still added to the first available armor inventory slot.
* The purchase price is still appended to the stored armor entry.
* Purchased armor is still marked as `sold` in `armor.json`.
* Invalid armor keys still return the legacy rejection message.
* Already sold armor still returns the legacy sold message.
* Buyers without enough renown still receive the legacy insufficient-renown message.
* Buyers with full armor inventories still receive the legacy inventory-space message.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* `armor.json` loading and saving remain in `original/onPRIUtils.py`.
* Armor selling, armor naming, equipping, unequipping, potion use, potion transfer, combat behavior, XP payout,
renown payout, and level-up handling were not changed by this extraction.

Tests added or expanded:

* `tests/test_armor_repository.py`
* `tests/test_legacy_onpriutils_buyarmor.py`

Status:

* Complete.

---

### Armor Sale Extraction

Completed helper:

* `sell_character_armor()` in `src.armor_repository`

Legacy wrapper:

* `pri_10_sellarmor()` now delegates deterministic armor sale-state mutation to `sell_character_armor()` while keeping
file loading and saving in `original/onPRIUtils.py`.

Behavior preserved:

* Owned armor can still be sold for half the stored purchase price.
* The seller's renown is still increased by the half-price refund.
* The sold armor slot is still set to `"n/a"`.
* Equipped armor still cannot be sold.
* Missing armor keys still return the legacy rejection message.
* Legacy armor inventory key-normalization behavior is preserved.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* Armor naming, equipping, unequipping, potion use, potion transfer, combat behavior, XP payout, renown payout, and
level-up handling were not changed by this extraction.

Tests added or expanded:

* `tests/test_armor_repository.py`
* `tests/test_legacy_onpriutils_sellarmor.py`

Status:

* Complete.

---

### Armor Equipment Lifecycle Boundary Audit

Completed test coverage:

* `pri_10_namearmor()` legacy armor naming behavior
* `pri_6_equip()` legacy armor equip behavior
* `pri_8_unequip()` legacy armor unequip behavior

Behavior documented and preserved:

* Missing-character rejection is covered for armor naming, equipping, and unequipping.
* Armor naming still rejects missing armor inventory keys.
* Armor naming still rejects duplicate destination names.
* Armor naming still rejects currently equipped armor.
* Valid armor naming still renames the armor dictionary key while preserving the stored armor value.
* Equipping armor is still blocked while a fight is active.
* Valid armor equip still clears previous armor bonus fields, sets `equip`, and applies armor bonuses from `armor.json`.
* Invalid armor equip still clears existing armor bonus fields before returning the legacy missing-armor message.
* Unequipping armor is still blocked while a fight is active.
* Valid armor unequip still clears `equip` and all armor bonus fields.
* Legacy unequip behavior still does not require the named armor to exist before clearing equipped armor and armor bonuses.
* The `pri_6_equip()` `armorDictionary` variable mismatch was corrected so the delegated armor dictionary loader is usable by the existing legacy equip logic.

Tests added or expanded:

* `tests/test_legacy_onpriutils_armor_lifecycle.py`

Status:

* Audit and legacy behavior coverage complete.
* Equipment lifecycle extraction has been completed and is covered by repository and legacy wrapper tests.

---

### Armor Equipment Lifecycle Extraction

Completed helpers:

* `rename_character_armor()` in `src.armor_repository`
* `unequip_character_armor()` in `src.armor_repository`
* `equip_character_armor()` in `src.armor_repository`

Legacy wrappers:

* `pri_10_namearmor()` now delegates deterministic armor rename logic to `rename_character_armor()`.
* `pri_8_unequip()` now delegates deterministic armor unequip logic to `unequip_character_armor()`.
* `pri_6_equip()` now delegates deterministic armor equip logic to `equip_character_armor()`.

Behavior preserved:

* Armor naming still rejects missing armor inventory keys.
* Armor naming still rejects duplicate destination names.
* Armor naming still rejects currently equipped armor.
* Valid armor naming still renames the armor dictionary key while preserving the stored armor value.
* Missing-character rejection remains handled in the legacy wrappers.
* Equipping armor is still blocked while a fight is active.
* Valid armor equip still clears previous armor bonus fields, sets `equip`, and applies armor bonuses from `armor.json`.
* Invalid armor equip still clears existing armor bonus fields before returning the legacy missing-armor message.
* Armor equip still applies Strength, Dexterity, Constitution, HP, AC, hit, damage, blur, initiative, and DR armor bonuses using the legacy stat-code behavior.
* Armor DR still only applies when both `traitdr` and `regeneration` are `0`.
* Armor initiative still writes both `armorinitiative` and `initiative`.
* Unequipping armor is still blocked while a fight is active.
* Valid armor unequip still clears `equip` and all armor bonus fields.
* Legacy unequip behavior still does not require the named armor to exist before clearing equipped armor and armor bonuses.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* `armor.json` loading remains in `original/onPRIUtils.py` for equip behavior.
* Potion use, potion transfer, combat behavior, rolling, XP payout, renown payout, and level-up handling were not changed by this extraction.

Tests added or expanded:

* `tests/test_armor_repository.py`
* `tests/test_legacy_onpriutils_armor_lifecycle.py`

Status:

* Complete.

---

### Character View Display Formatting Modernization

Completed helpers:

* `build_character_view_message()` in `src.character_repository`

Legacy wrapper:

* `pri_viewchar()` now delegates character sheet display construction to `build_character_view_message()`.
* `pri_viewchar()` still loads the character file through the character repository helper.
* `pri_viewchar()` still builds the view context through `build_character_view_context()`.
* `pri_viewchar()` still applies recalculated totals through `apply_character_view_totals()`.
* `pri_viewchar()` still saves the updated character data after applying view totals.

Behavior deliberately changed:

* The old GUI-oriented character sheet display was replaced with cleaner plain-text output intended to fit Discord better.
* Fragile stylized Unicode labels, color tags, and tab-heavy display alignment were removed from the character view output.
* The new display groups character information into readable sections: Core, Attributes, Combat Summary, Progress, Record, and Inventory.

Behavior preserved:

* Missing-character handling remains in `pri_viewchar()`.
* Character file loading and saving remain in `original/onPRIUtils.py`.
* Character view context construction remains in `src.character_repository.build_character_view_context()`.
* Character view total calculation remains in the repository-backed view total helper.
* Total write-back for `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration` remains preserved.
* Combat behavior, rolling, XP payout, renown payout, level-up handling, potion behavior, armor behavior, 
inventory/economy behavior, leaderboard behavior, who behavior, player-score behavior, and wholevel behavior were not changed.

Cleanup completed:

* A duplicate earlier `build_character_view_context()` definition was removed from `src.character_repository`.
* The remaining active `build_character_view_context()` definition is the full context builder used by `pri_viewchar()`.

Tests added or expanded:

* `tests/test_legacy_onpriutils_viewchar.py`

Verification:

* `pytest tests/test_legacy_onpriutils_viewchar.py`
* `pytest`

Status:

* Complete.

### Character View Total Write-Back Orchestration Extraction

Completed helper:

* `build_and_save_character_view()` in `src.character_repository`

Legacy wrapper:

* `pri_viewchar()` now delegates the character load, view context construction, display message construction, total application, and character save sequence to `build_and_save_character_view()`.
* `pri_viewchar()` still owns the missing-character check and private command return shape.

Behavior preserved:

* Using `!viewchar` still refreshes saved combat-facing totals on the character file.
* Character view total calculation remains delegated to `calculate_character_view_totals()`.
* Character view context construction remains delegated to `build_character_view_context()`.
* Character view display construction remains delegated to `build_character_view_message()`.
* Total write-back for `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration` remains preserved.
* Combat still depends on these saved fields during challenge setup, initiative, attack rolls, armor class checks, damage, damage reduction, and regeneration.
* Combat freshness behavior was not changed. Automatic recalculation at challenge or combat start remains a separate risk area.
* Combat behavior, rolling, XP payout, renown payout, level-up handling, potion behavior, armor behavior, 
  inventory/economy behavior, leaderboard behavior, who behavior, player-score behavior, wholevel behavior, and character view display formatting were not changed.

Tests:

* Existing `tests/test_legacy_onpriutils_viewchar.py` coverage continues to verify missing-character behavior,
  displayed output, and saved total write-back for strength, dexterity, and constitution builds.

Verification:

* `pytest tests/test_legacy_onpriutils_viewchar.py`
* `pytest`

Status:

* Complete.

## Remaining Function Risk Review

### Extracted Inventory and Economy Boundaries

#### `pri_9_buyarmor`

Status:

* Extracted.

Completed helper:

* `buy_character_armor()` in `src.armor_repository`

Notes:

* File loading and saving remain in the legacy wrapper.
* Armor selling, armor naming, equipping, unequipping, potion use, potion transfer, combat behavior, XP payout,
renown payout, and level-up handling were not changed by the purchase extraction.

---

#### `pri_10_sellarmor`

Status:

* Extracted.

Completed helper:

* `sell_character_armor()` in `src.armor_repository`

Notes:

* File loading and saving remain in the legacy wrapper.
* Armor sale still refunds half the stored purchase price.
* Equipped armor still cannot be sold.
* Missing armor keys still return the legacy rejection message.
* Legacy armor inventory key-normalization behavior is preserved.
* Armor naming, equipping, unequipping, potion use, potion transfer, combat behavior, XP payout, renown payout, and
level-up handling were not changed by the sale extraction.

---

#### `pri_10_namearmor`

Status:

* Extracted.

Completed helper:

* `rename_character_armor()` in `src.armor_repository`

Notes:

* File loading and saving remain in the legacy wrapper.
* Armor rename still rejects missing armor inventory keys.
* Armor rename still rejects duplicate destination names.
* Armor rename still rejects currently equipped armor.
* Valid armor rename still preserves the stored armor value while changing the inventory key.
* Armor buying, armor selling, equipping, unequipping, potion use, potion transfer, combat behavior, XP payout,
renown payout, and level-up handling were not changed by the rename extraction.

---

#### `pri_6_equip`

Status:

* Extracted.

Completed helper:

* `equip_character_armor()` in `src.armor_repository`

Notes:

* File loading and saving remain in the legacy wrapper.
* `armor.json` loading remains in the legacy wrapper.
* Valid armor equip still clears prior armor bonuses, sets `equip`, and applies armor stat bonuses.
* Invalid armor equip still clears armor bonus fields before returning the legacy missing-armor message.
* Armor DR still only applies when both `traitdr` and `regeneration` are `0`.
* Armor initiative still updates both `armorinitiative` and `initiative`.
* Potion use, potion transfer, combat behavior, rolling, XP payout, renown payout, and level-up handling were not
changed by the equip extraction.

---

#### `pri_8_unequip`

Status:

* Extracted.

Completed helper:

* `unequip_character_armor()` in `src.armor_repository`

Notes:

* File loading and saving remain in the legacy wrapper.
* Unequip still clears `equip` and all armor bonus fields.
* Legacy unequip behavior still does not validate that the named armor exists.
* Potion use, potion transfer, combat behavior, rolling, XP payout, renown payout, and level-up handling were not
changed by the unequip extraction.

---

#### `pri_10_usepotion`

Status:

* Extracted.

Completed helpers:

* `use_character_potion()` in `src.potion_repository`
* `_apply_permanent_stat_potion()` in `src.potion_repository`

Notes:

* File loading and saving remain in the legacy wrapper.
* Permanent stat potion progression is consolidated behind `_apply_permanent_stat_potion()`.
* Permanent stat potion success, invalid progression rejection, and inventory removal behavior are preserved.
* `respec` and `stimulant` behavior are preserved.
* Temporary potion behavior remains inside `use_character_potion()` and has not been split further.
* The regeneration potion inventory-removal bug is intentionally preserved.
* Valid potion names missing from character inventory can still raise `ValueError`.
* Unknown potion names still return the legacy unknown-potion message.
* Combat behavior, rolling, XP payout, renown payout, and level-up handling were not changed by the potion use extraction or cleanup review.

---

### High Risk Remaining Targets

No additional inventory or economy extraction target is currently selected.

The previous high-risk potion use target has been extracted and cleaned up. Any future potion cleanup should
begin with a dedicated audit before code changes, especially if it involves temporary potion behavior, regeneration
behavior, combat-adjacent potion fields, or inventory-removal quirks.


## Explicitly Out of Scope

The following remain out of scope for this audit pass unless deliberately selected with a new test plan:

* `message_8_usefeat`
* `message_5_pass`
* `message_roll`
* `Roll_true_strike.py`
* `Roll_not_strike.py`
* `playerone_zero_current_hp.py`
* `playertwo_zero_current_hp.py`
* `feat_methods.py`
* Combat win/loss resolution
* XP payout logic
* Renown payout logic
* Level-up handling
* Rolling resolution
* Combat feat execution
* Full potion lifecycle changes
* Equipment behavior changes

---

## Recommended Next Target

Recommended next step:

* Pause additional inventory and economy extraction until the next target is deliberately selected.

Reason:

* Armor purchase, armor sale, armor naming, armor equip, and armor unequip are now extracted and tested.
* Potion purchase, potion sale, potion shop restocking, potion transfer, and potion use are now extracted and tested.
* Permanent stat potion progression cleanup is complete and tested.
* Read-only shop display routing has no remaining active extraction target.
* Leaderboard, who, player-score, and wholevel behavior are sufficiently extracted and tested for the current phase.
* Character view display formatting has been extracted and modernized for Discord-readable output.
* Remaining work is more likely to touch combat-adjacent behavior, broader command/runtime behavior, or fragile legacy quirks.

Possible next audit targets:

* Combat-adjacent potion effect cleanup, only after a dedicated test plan is written.
* Character view total recalculation/write-back behavior, only if deliberately selected as a focused mutation-boundary audit.
* Combat summary field freshness, only if the project is ready to examine whether combat should rely on
  saved `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration` values.

Read-only shop display routing audit result:

* Inventory and economy command routing remains in `original/botCommand.py`.
* `!armorshop` no longer opens `armor.json` directly in `botCommand.py`.
* `!armorshop` no longer builds the armor display input list in `botCommand.py`.
* `!armorshop` now delegates armor data loading and shop body construction to `pri_armorshop()`.
* `pri_armorshop()` loads armor data through `src.armor_repository.get_armor_dictionary()`.
* `pri_armorshop()` builds the armor display input list from `armor_dictionary[0]["armorlist"]`.
* `pri_10_armorshop()` delegates armor display body formatting to `src.armor_repository.build_armor_shop_display()`.
* `botCommand.py` still owns the `!armorshop` display header and private response routing.
* `!potionshop` no longer opens `potions.json` directly in `botCommand.py`.
* `pri_potionshop()` loads potion data through `src.potion_repository.get_potion_dictionary()`.
* `src.potion_repository.build_potion_shop_display()` now owns duplicate counting, rarity price lookup, first-seen
  shop order preservation, and final potion shop body line construction.
* `botCommand.py` still owns the `!potionshop` display header and private response routing.
* No shop display extraction target remains active.

Remaining inventory/economy boundary review result:

* `original/botCommand.py` no longer directly opens `potions.json` or `armor.json`.
* `!potionshop` routes through `pri_potionshop()`.
* `!armorshop` routes through `pri_armorshop()`.
* Remaining direct `potions.json` and `armor.json` access is limited to legacy PRI wrappers, repository/data-loader code, and tests.
* Remaining `original/onPRIUtils.py` direct JSON access is tied to legacy wrapper file loading and saving for
  shop stocking, potion buying/selling/using, armor buying/selling/equipping, inventory updates, renown updates, and shop depletion.
* No further read-only shop display boundary remains in `original/botCommand.py`.
* Further inventory/economy extraction should continue only through a focused mutation-boundary pass with temporary test files and no live data access.

Leaderboard and character summary display boundary review result:

* `!leaderboard` routing remains in `original/botCommand.py`.
* `message_12_leaderboard()` in `original/onMSGUtils.py` already delegates leaderboard display construction to `src.character_repository.build_character_leaderboard_messages()`.
* `build_character_leaderboard_messages()` owns the current leaderboard file-loading, win/loss/percent calculation, sorting, and display-line formatting.
* Repository tests already cover leaderboard sorting by wins, losses, percent, default sorting behavior, and zero-match percent handling.
* `!who` routing remains in `original/botCommand.py`, while character-summary score behavior is already covered by repository and legacy tests.
* `!player` remains commented out in `original/botCommand.py`; related score-display helper behavior still has tests, but the public command route is dead legacy routing.
* `!wholevel` routing remains in `original/botCommand.py`, with repository and legacy tests covering the extracted behavior.
* `pri_viewchar()` still displays wins, losses, and forfeits from the view context, but the character sheet display body now delegates to `src.character_repository.build_character_view_message()`.
* `build_character_view_message()` owns the Discord-readable character sheet display format.
* `pri_viewchar()` still owns character file loading, view total application, character saving, and command return orchestration.
* Combat result mutations that increment wins, losses, and forfeits remain in combat-result files and `botCommand.py`;
  those are expected mutation hits and are out of scope for this display-boundary review.
* Feat percentage hits in `original/feat_methods.py` are unrelated combat percentage logic and are out of scope for leaderboard and character summary display extraction.

Conclusion:

* No new leaderboard, who, player-score, wholevel, or character view display extraction is recommended at this time.
* This area is sufficiently extracted and tested for the current refactor phase.
* Any future `pri_viewchar()` work should focus only on the mutation-bearing total recalculation/write-back boundary, not display formatting.
* Character view total write-back orchestration extraction complete.

### Combat Saved-Total Dependency Review

Search-only review completed for saved combat-facing totals:

* `thp`
* `tac`
* `tdr`
* `thit`
* `tdamage`
* `initiative`
* `regeneration`

Current behavior:

* `!viewchar` remains the saved-total refresh boundary.
* `!challenge` snapshots player one combat HP from saved `pOneInfo["thp"]`.
* `!accept` snapshots player two combat HP from saved `pTwoInfo["thp"]`.
* Challenge acceptance and initiative resolution use saved `initiative` values.
* Roll handling uses saved `thit`, `tac`, `tdr`, `tdamage`, and `regeneration` values from the loaded player info.
* True Strike and normal strike paths both read saved combat-facing totals.
* Evasion/pass/deflect-style combat branches also read saved `regeneration`.
* Combat setup does not recalculate character totals before storing combat state.
* Combat roll handling does not recalculate character totals before resolving attacks.

Saved-total write-back source:

* `src.character_repository.apply_character_view_totals()` writes `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration`.
* `src.character_repository.build_and_save_character_view()` is the repository-backed orchestration helper that loads the character, builds the character view context, builds the display message, applies calculated totals, and saves the character.
* `original/onPRIUtils.py::pri_viewchar()` remains the legacy command boundary that triggers that refresh.

Confirmed combat dependencies:

* Challenge setup dependency: `!challenge` and `!accept` copy saved `thp` into combat total/current HP state.
* Initiative dependency: challenge acceptance compares saved `initiative`.
* Attack roll dependency: normal roll handling reads saved `thit`.
* Armor class dependency: normal roll handling reads saved `tac`.
* Damage dependency: normal and True Strike handling read saved `tdamage`.
* Damage reduction dependency: normal roll, True Strike, and stoneskin/DR helper paths read saved `tdr`.
* Regeneration dependency: normal roll, True Strike, pass/evasion handling, and regeneration helper paths read saved `regeneration`.

Confirmed stale-total mutation sources:

* Stat selection changes strength, dexterity, constitution, and initiative-facing data.
* Build selection changes the formula used to calculate combat totals.
* Trait selection changes trait hit, damage, AC, DR, HP, regeneration, and initiative-facing data.
* Feat selection changes feat hit, damage, AC, HP, and other combat-facing behavior.
* Armor equip and unequip change armor hit, damage, AC, HP, DR, initiative, strength, dexterity, constitution, and blur fields.
* Potion use changes potion hit, damage, AC, HP, strength, dexterity, constitution, regeneration, and blur fields.
* Permanent stat potion use changes permanent strength, dexterity, and constitution fields.
* Potion cleanup after combat resets temporary potion fields.
* Level-up handling changes HP, base damage, hit, damage, AC, feat slots, ability point state, and trait scaling fields.
* Ability point add changes strength, dexterity, or constitution and explicitly tells the player to run `!viewchar` to ensure changes.

Risk classification:

* This is a risky behavior area because combat currently relies on saved totals rather than recalculating from source fields at combat start.
* The current legacy contract appears to be that players must run `!viewchar` after character-changing actions to refresh combat-facing totals.
* Changing challenge setup to automatically refresh totals would be a behavior change.
* Changing roll handling to automatically refresh totals would be a larger combat behavior change.
* Changing potion cleanup, armor equip, trait selection, feat selection, stat selection, level-up, or ability point
  add to automatically refresh totals would also be behavior-changing because it would alter when combat-facing saved totals become current.

Expected test coverage:

* Existing view character tests cover saved-total write-back for strength, dexterity, and constitution builds.
* Existing apply-view-total tests cover the direct total write-back helper.
* Existing challenge acceptance tests cover initiative behavior using provided saved initiative values.
* Existing armor, potion, trait, feat, stat, and ability-point tests cover the mutation sources themselves.
* No current test should be assumed to enforce automatic combat freshness.
* Any future combat freshness change needs explicit tests proving the old stale-total behavior first, then deliberate tests for the selected new behavior.

Combat saved-total contract test coverage result:

* Added focused test coverage documenting the current saved-total combat contract.
* Challenge acceptance initiative resolution is covered as using saved `initiative` values directly.
* Challenge acceptance is covered as returning loaded player two character data with saved `thp` intact, even when recalculated view totals would differ.
* Ability point mutation is covered as updating the source ability score while preserving saved combat-facing totals until character view refresh.
* This coverage documents current legacy behavior only; it does not change combat freshness, rolling behavior, mutation behavior, or character view total write-back behavior.

Combat saved-total refresh helper extraction result:

* Added `src.character_repository.refresh_character_combat_totals()` as a repository-level helper for refreshing one character's saved combat-facing totals.
* The helper loads the character from the supplied character directory, calculates totals through `calculate_character_view_totals()`,
  applies saved combat-facing totals through `apply_character_view_totals()`, saves the character, and returns the refreshed character data.
* The helper is intentionally not wired into `!viewchar`, `!challenge`, `!accept`, `!roll`, or `original/botCommand.py`.
* Combat behavior remains unchanged. Existing combat continues to rely on saved combat-facing totals already present on the character sheet.
* Added repository tests proving the helper updates `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration` using temporary character files only.

Combat refresh helper wiring audit result:

* `src.character_repository.refresh_character_combat_totals()` remains a repository-only helper.
* No behavior wiring was added during this audit.
* `!viewchar` still refreshes saved combat-facing totals through `build_and_save_character_view()`.
* `!challenge` still snapshots player one combat HP from saved `thp`.
* `!accept` still loads player two data and resolves initiative from saved `initiative`.
* `!accept` still snapshots player two combat HP from saved `thp`.
* `!roll` still operates on already-loaded combat state and should not be the first refresh wiring point.
* Future wiring directly at combat entry would change the current legacy contract that character-changing commands require a later refresh before combat.
* Future wiring after mutation commands is safer than refreshing during combat, but it should be done one command at a time with contract tests.
* Candidate mutation commands that can make saved combat-facing totals stale include `!stats`, `!build`, `!traitpick`,
  `!featpick`, `!add`, `!respec`, `!usepotion`, `!equip`, `!unequip`, and post-combat level-up handling.
* A narrow future target would be one mutation command such as `!add`, because existing coverage already documents
  that source ability changes preserve saved combat-facing totals until refresh.

Combat saved-total recommendation:

* Do not change combat freshness behavior in this pass.
* Do not introduce automatic total recalculation at `!challenge`, `!accept`, or `!roll` yet.
* Do not change combat, rolling, payout, potion cleanup, level-up, armor, potion, inventory/economy, leaderboard, who, player-score, wholevel, or character view display behavior.
* A repository helper for explicit total refresh may be considered later, but it should not be wired into combat until a deliberate behavior change is selected.

Recommendation:

* Pause additional inventory and economy extraction until the next target is deliberately selected.
* Skip leaderboard, who, player-score, and wholevel extraction for now because those areas are already sufficiently extracted and tested.
* Do not split temporary potion behavior further without a focused audit.
* Keep file loading and saving in `original/onPRIUtils.py` unless a file-boundary change is explicitly planned.
* Do not import `original/botCommand.py` in pytest.
* Do not touch combat behavior, rolling, XP payout, renown payout, or level-up handling.

Status:

* Potion use lifecycle extraction complete.
* Potion use cleanup review complete.
* Temporary potion behavior repository coverage expanded.
* Temporary potion behavior legacy wrapper coverage expanded.
* Temporary potion edge-case repository coverage expanded.
* Temporary potion regeneration no-benefit wrapper coverage expanded.
* Remaining inventory/economy boundary review complete.
* Duplicate character view context definition cleanup complete.
* Character view display formatting modernization complete.
* Character view display wrapper coverage updated.
* Combat saved-total contract test coverage complete.

---

Ability point refresh wiring implementation result:

* `pri_4_add()` now refreshes saved combat-facing totals immediately after a successful ability-point spend.
* The refresh is limited to the successful `!add` path after `add_ability_point()` mutates the source ability and clears `apboost`.
* Invalid ability requests return before loading or refreshing the character file.
* Valid requests without `apboost` preserve stale saved combat-facing totals and return the existing no-points message.
* Focused coverage confirms strength, dexterity, and constitution spends refresh saved combat-facing totals without
  touching combat, rolling, challenge, accept, potion cleanup, armor behavior, feat behavior, trait behavior, stat
  behavior, XP payout, renown payout, level-up handling, leaderboard, who, player-score, wholevel, or character view display formatting.

Initial stat refresh wiring implementation result:

* `pri_6_stats()` now refreshes saved combat-facing totals immediately after successful first-time stat assignment.
* The refresh is limited to the successful `!stats` path after `assign_character_stats()` mutates the source strength,
  dexterity, constitution, ability bonus, HP bonus, AC bonus, and initiative fields.
* Failed stat assignment paths preserve stale saved combat-facing totals.
* Focused coverage confirms successful stat assignment refreshes saved `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration`.
* Focused coverage confirms rejected total-point assignment and already-assigned stat cases do not refresh stale saved combat-facing totals.
* This implementation does not touch combat, rolling, challenge, accept, potion cleanup, armor behavior, feat behavior,
  trait behavior, XP payout, renown payout, level-up handling, leaderboard, who, player-score, wholevel, or character view display formatting.

Trait refresh wiring implementation result:

* `pri_6_trait()` now refreshes saved combat-facing totals immediately after successful first-time trait selection.
* The refresh is limited to the successful `!traitpick` path after `select_character_trait()` mutates the selected trait and related trait/source bonus fields.
* Failed trait selection paths preserve stale saved combat-facing totals.
* Focused coverage confirms successful trait selection refreshes saved `thp`, `tac`, `tdr`, `thit`, `tdamage`, `initiative`, and `regeneration`.
* Focused coverage confirms invalid trait selection and already-selected trait cases do not refresh stale saved combat-facing totals.
* Existing wrapper delegation coverage now patches the imported `original.onPRIUtils.select_character_trait` binding
  directly, matching how the wrapper actually calls the dependency.
* This implementation does not touch combat, rolling, challenge, accept, potion cleanup, armor behavior, feat behavior,
  stat behavior, ability-point behavior, XP payout, renown payout, level-up handling, leaderboard, who, player-score, wholevel, or character view display formatting.

Recommendation:

* Do not change combat freshness behavior in this pass.
* Do not wire `refresh_character_combat_totals()` into `!challenge`, `!accept`, or `!roll`.
* Do not change `!viewchar`, potion cleanup, armor behavior, feat behavior, trait behavior, stat behavior, XP payout,
  renown payout, level-up handling, leaderboard, who, player-score, wholevel, or character view display formatting.
* If this work continues, the safest next step is another single mutation command with stale-total contract coverage first.

## Update Procedure for Future Work

When another inventory or economy boundary is completed, update this audit in the following order:

1. Run the full test suite and update only `## Current Test Status` with the latest result.
2. Add the completed area to `## Current Position`.
3. Add one new subsection under `## Completed Extractions`.
4. Move the completed function out of the active risk list and into `### Extracted Inventory and Economy Boundaries`
   if it belongs there.
5. Update `## Recommended Next Target` to reflect the next audit or extraction target.
6. Do not keep old full pytest totals inside older completed extraction sections.
7. Do not add chapter labels or chapter numbers to this audit file.

