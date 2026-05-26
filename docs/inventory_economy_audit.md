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

* `323 passed`



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
covers read-only display behavior, shop restocking behavior, single-character potion economy behavior, armor purchase
behavior, armor sale behavior, and armor equipment lifecycle boundary behavior.

Completed inventory/economy areas include:

* Read-only armor shop display
* Single-character potion sale
* Potion shop restock
* Potion purchase
* Armor shop restock
* Armor purchase
* Armor sale
* Armor equipment lifecycle boundary audit

Repository-backed helpers now exist for:

* Building armor shop display text
* Selling potions
* Restocking the potion shop
* Buying potions
* Restocking the armor shop
* Buying armor
* Selling armor

Remaining targets are higher risk because they touch armor inventory keys, equipment state, combat-facing fields,
multiple character files, permanent potion progression, or potion lifecycle behavior.

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
* Legacy F-list color tags and output formatting are preserved.
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
* No equipment lifecycle extraction has been performed yet.

---

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

### Medium-to-High Risk Remaining Targets

#### `pri_10_namearmor`

Classification:

* Equipment inventory key mutation
* Character-file mutation

Reason:

* Renames keys inside the armor inventory dictionary.
* Can affect sell, equip, unequip, and view behavior.
* Rejects renaming currently equipped armor.
* Should be reviewed together with equip and unequip behavior before extraction.

Recommendation:

* Covered by armor equipment lifecycle legacy tests.
* Safe extraction candidate only if moved together with the other armor lifecycle helpers or after a dedicated repository helper plan is written.

---

#### `pri_11_givepotion`

Classification:

* Inventory transfer mutation
* Multi-character file mutation

Reason:

* Mutates two character files.
* Removes a potion from the gifter.
* Adds a potion to the recipient.
* Depends on recipient inventory capacity behavior.
* Partial-write failures would be dangerous.

Recommendation:

* Defer until single-character inventory behavior remains stable and a dedicated transfer plan is written.

---

### High Risk Remaining Targets

#### `pri_6_equip`

Classification:

* Equipment state mutation
* Combat-adjacent stat mutation
* Character-file mutation

Reason:

* Mutates combat-facing armor bonus fields.
* Sets equipped armor.
* Resets and reapplies armor bonuses.
* Interacts with initiative, HP, AC, damage, hit, DR, blur, Strength, Dexterity, and Constitution fields.
* Depends on armor inventory key behavior and should not be separated from a broader equipment lifecycle review.

Recommendation:

* Covered by armor equipment lifecycle legacy tests.
* High risk due to combat-facing stat fields.
* Extract only after the repository helper boundary is planned carefully.

---

#### `pri_8_unequip`

Classification:

* Equipment state mutation
* Combat-adjacent stat mutation
* Character-file mutation

Reason:

* Clears equipped armor.
* Resets armor bonus fields.
* Simpler than equip, but logically tied to equip behavior.
* Should be reviewed with equip rather than extracted in isolation.

Recommendation:

* Covered by armor equipment lifecycle legacy tests.
* Lower risk than equip, but still tied to the same equipment lifecycle boundary.
* Extract only after the repository helper boundary is planned carefully.

---

#### `pri_10_usepotion`

Classification:

* Potion lifecycle mutation
* Temporary combat modifier setup
* Permanent character progression mutation
* Character-file mutation
* Combat-adjacent behavior

Reason:

* Applies permanent stat potion progression.
* Applies respec and stimulant potion behavior.
* Applies temporary next-match potion effects.
* Mutates potion effect fields used by later view and combat logic.
* Removes consumed potions from inventory.

Recommendation:

* Defer to a dedicated potion lifecycle pass.

---

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
* Full armor lifecycle changes
* Equipment behavior changes

---

## Recommended Next Target

## Recommended Next Target

Recommended next step:

* Decide whether to extract armor equipment lifecycle helpers into `src.armor_repository`.

Reason:

* Armor purchase and armor sale are already extracted and tested.
* Armor naming, equipping, and unequipping now have legacy behavior coverage.
* The remaining armor lifecycle functions are still in `original/onPRIUtils.py`.
* `pri_10_namearmor` mutates armor inventory keys.
* `pri_6_equip` mutates combat-facing armor bonus fields.
* `pri_8_unequip` clears equipped armor and all armor bonus fields.
* Equipment lifecycle extraction should be handled deliberately and should preserve the documented legacy side effects.

Possible next implementation targets:

* `rename_character_armor()`
* `equip_character_armor()`
* `unequip_character_armor()`

Recommendation:

* If extraction begins, write repository tests first.
* Keep file loading and saving in `original/onPRIUtils.py`.
* Do not import `original/botCommand.py` in pytest.
* Do not touch potion use, potion transfer, combat behavior, rolling, XP payout, renown payout, or level-up handling.

Status:

* Armor equipment lifecycle boundary audit complete.
* Next step may be a focused armor lifecycle extraction plan.

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
