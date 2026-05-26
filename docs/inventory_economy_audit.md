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

* `377 passed`

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

Completed inventory/economy areas include:

* Read-only armor shop display
* Single-character potion sale
* Potion shop restock
* Potion purchase
* Potion transfer
* Potion use lifecycle extraction
* Potion use cleanup review
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

* `pri_11_givepotion()` now delegates deterministic potion transfer-state mutation to `give_character_potion()` while keeping both character-file loads and both character-file writes in `original/onPRIUtils.py`.

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
* Potion purchase, potion sale, potion use, potion restocking, armor behavior, combat behavior, rolling, XP payout, renown payout, and level-up handling were not changed by this extraction.

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

* `pri_10_usepotion()` now delegates potion mutation and message behavior to `use_character_potion()` while keeping character-file loading and saving in `original/onPRIUtils.py`.

Behavior preserved:

* Permanent progression potions are preserved: `str1` through `str5`, `dex1` through `dex5`, and `con1` through `con5` still mutate `pstrength`, `pdexterity`, or `pconstitution` only when the existing progression field is exactly one tier lower.
* Permanent stat potion progression has been consolidated into `_apply_permanent_stat_potion()`.
* `_apply_permanent_stat_potion()` preserves the legacy success message, inventory removal behavior, and invalid-progression rejection message.
* `respec` still increments `reset`.
* `stimulant` still increments both `remaining feats` and `total feats`.
* Temporary next-match potions still set the matching potion bonus field and usually set `potioneffect`.
* Valid potion names are still checked through potion data lookup, not against character inventory before use. A valid potion name missing from inventory can still raise `ValueError` when removal is attempted.
* Unknown potion names still return `You do not have a potion of <potion>`.
* A character with an existing `potioneffect` still cannot drink another temporary potion.
* Permanent stat potions, `respec`, and `stimulant` are still handled before the temporary potion lock.
* Regeneration potions still set `potionregen` and `potioneffect`, but the successful branch still does not remove the potion from inventory.
* The regeneration eligibility condition still uses `traitdr == 0 or armordr == 0 or regeneration == 0`, which means the potion is blocked only when all three fields are nonzero.
* Existing messages, typos, spacing, field names, and questionable conditionals remain preserved.

Cleanup review result:

* The permanent stat potion progression block was the only safe cleanup boundary selected after extraction.
* Temporary potion behavior was intentionally left inside `use_character_potion()` because it contains fragile legacy behavior and combat-adjacent state setup.
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
* Remaining work is more likely to touch combat-adjacent behavior, broader command/runtime behavior, or fragile legacy quirks.

Possible next audit targets:

* Temporary potion behavior legacy wrapper coverage review, if more potion cleanup is desired.
* Remaining command-runtime inventory routing in `botCommand.py`, if direct runtime behavior needs to be mapped.
* Combat-adjacent potion effect cleanup, only after a dedicated test plan is written.

Recommendation:

* Do not split temporary potion behavior further without a focused audit.
* Keep file loading and saving in `original/onPRIUtils.py` unless a file-boundary change is explicitly planned.
* Do not import `original/botCommand.py` in pytest.
* Do not touch combat behavior, rolling, XP payout, renown payout, or level-up handling.

Status:

* Potion use lifecycle extraction complete.
* Potion use cleanup review complete.
* Temporary potion behavior repository coverage expanded.
* Full pytest passes with 377 tests.

---

## Update Procedure for Future Work

When another inventory or economy boundary is completed, update this audit in the following order:

1. Run the full test suite and update only `## Current Test Status` with the latest result.
2. Add the completed area to `## Current Position`.
3. Add one new subsection under `## Completed Extractions`.
4. Move the completed function out of the active risk list and into `### Extracted Inventory and Economy Boundaries` if it belongs there.
5. Update `## Recommended Next Target` to reflect the next audit or extraction target.
6. Do not keep old full pytest totals inside older completed extraction sections.
7. Do not add chapter labels or chapter numbers to this audit file.
