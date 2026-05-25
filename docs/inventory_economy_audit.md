# Inventory and Economy Audit

## Purpose

This audit tracks the next refactor direction after the character repository cleanup pass.

The character repository pass is complete. No additional low-risk character repository extraction target remains. Potion, armor, equipment, inventory, shop, economy, and combat-adjacent behavior should not be changed until their boundaries are mapped and tested.

The goal of this audit is to identify the safest next extraction target without changing runtime behavior.

The guiding rules for this audit are:

- Write tests before changing behavior.
- Do not import `original/botCommand.py` in pytest.
- Use temporary test directories and temporary JSON files.
- Do not touch live character data.
- Preserve legacy behavior exactly.
- Do not change rolling resolution.
- Do not change combat win/loss resolution.
- Do not change XP payout.
- Do not change renown payout.
- Do not change combat feat execution.
- Do not change potion lifecycle behavior during the audit.
- Do not change armor lifecycle behavior during the audit.
- Do not change equipment behavior during the audit.
- Do not change level-up handling during the audit.

---

## Current Starting Point

The previous character repository audit concluded that the safest character-related cleanup pass is complete.

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
- Active character master-list construction
- Remaining low-risk boundary audit

`botCommand.py` is still not imported directly in pytest because of runtime dependencies.

The remaining simple helpers in `original/onMSGUtils.py` are deprecated flavor/message helpers rather than meaningful repository behavior.

Further `message_accept` cleanup remains medium-risk and should wait unless deliberately selected with a separate test plan.

---

## Audit Scope

This audit focuses on inventory, economy, potion, armor, shop, and equipment boundaries.

Primary files to review:

- `original/onPRIUtils.py`
- `src/potion_repository.py`
- `src/armor_repository.py`
- `potions.json`
- `armor.json`
- Existing potion repository tests
- Existing armor repository tests

Primary legacy functions to review:

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

---

## Classification Categories

Each function should be classified by the type of behavior it owns.

Use these categories:

### Read-Only Shop/List Display

Behavior that only reads shop data or character inventory and builds a message.

Possible lower-risk candidates may exist here if the function does not mutate character files.

### Purchase or Sale Economy Mutation

Behavior that changes renown, adds inventory, removes inventory, or calculates sale value.

This is higher risk because it changes persistent character state.

### Inventory Transfer Mutation

Behavior that moves potions, armor, or other inventory items between character sheets.

This is higher risk because it mutates more than one character file.

### Equipment State Mutation

Behavior that equips, unequips, names, or rewrites armor state.

This is high risk because it affects character totals and later combat-facing calculations.

### Temporary Combat Modifier Setup

Behavior that applies potion effects or temporary bonuses for a fight.

This is high risk because it touches combat-adjacent state.

### Permanent Character Progression Mutation

Behavior that permanently increases Strength, Dexterity, Constitution, regeneration, blur, HP, AC, hit, damage, DR, or similar character fields.

This is high risk because it overlaps character advancement and combat math.

### Combat-Adjacent Behavior

Behavior that affects fields used by combat, rolling, active feats, damage, defense, or end-of-fight cleanup.

This should not be extracted until the relevant behavior has dedicated tests.

---

## Initial Risk Expectations

### Lower Risk Candidates

These may be safer after inspection, but should still receive tests first:

- Read-only potion shop display
- Read-only armor shop display
- Read-only inventory display helpers, if any exist separately from mutation behavior

These are only lower risk if they do not mutate character files, renown, equipment, potion effects, armor effects, or combat-related fields.

### Medium Risk Candidates

These may be possible after the read-only boundaries are understood:

- Potion buying
- Potion selling
- Armor buying
- Armor selling

These require careful tests because they change renown and inventory state.

### High Risk Candidates

These should not be touched until later:

- Potion use
- Potion giving
- Armor naming
- Armor equipping
- Armor unequipping
- Any behavior that recalculates or mutates character combat totals
- Any behavior that applies temporary combat modifiers
- Any behavior that applies permanent stat progression

---

## Explicitly Out of Scope

The following must remain untouched during this audit:

- `message_8_usefeat`
- `message_5_pass`
- `message_roll`
- `Roll_true_strike.py`
- `Roll_not_strike.py`
- `playerone_zero_current_hp.py`
- `playertwo_zero_current_hp.py`
- `feat_methods.py`
- Combat win/loss resolution
- XP payout logic
- Renown payout logic
- Level-up handling
- Rolling resolution
- Combat feat execution
- Full potion lifecycle changes
- Full armor lifecycle changes
- Equipment behavior changes

---

## Current Decision

Do not begin implementation yet.

The next step is to audit the inventory and economy boundaries before choosing any extraction target.

The likely safest future implementation target should be read-only shop/list display behavior, assuming inspection confirms that the function does not mutate persistent character state.

Status:

- Audit started.

## Initial Function Boundary Review

### `pri_10_stockpotion`

Classification:

- Shop restock mutation
- Randomized shop generation
- Global data-file mutation

Behavior owned:

- Opens `potions.json` directly.
- Clears `potionDictionary[0]['shoplist']`.
- Randomly selects 20 potions from common, uncommon, rare, very rare, and relic lists.
- Writes the new shop list back to `potions.json`.
- Returns the stocked shop message and shop string.

Risk:

- Medium risk.

Reason:

- This does not touch character files directly.
- It does mutate shared shop data.
- It uses randomness, which means tests would need deterministic random control before extraction.

Recommendation:

- Do not extract first unless randomness is controlled in tests.
- Possible future repository target, but not the safest first implementation target.

---

### `pri_10_buypotion`

Classification:

- Purchase economy mutation
- Inventory mutation
- Global shop mutation

Behavior owned:

- Opens `potions.json`.
- Loads the buyer character sheet.
- Checks whether the potion is currently in the shop list.
- Calculates potion price from potion category data.
- Checks buyer renown.
- Checks potion inventory capacity.
- Subtracts renown from the buyer.
- Removes the potion from the shop list.
- Adds the potion to the character potion inventory.
- Writes the character file.
- Writes `potions.json`.

Risk:

- High risk.

Reason:

- This mutates both character data and global shop data.
- It changes renown and inventory state.
- It has multiple failure branches that must be preserved exactly.
- It should not be touched before dedicated tests exist.

Recommendation:

- Not a first extraction target.
- Needs repository tests using temporary character files and a temporary potion data file before any refactor.

---

### `pri_11_sellpotion`

Classification:

- Sale economy mutation
- Inventory mutation
- Character-file mutation

Behavior owned:

- Loads seller character sheet.
- Checks whether the seller owns the potion.
- Uses `get_potion_sell_value()` to calculate sale value.
- Adds renown to the seller.
- Removes the potion from seller inventory.
- Writes the seller character file.
- Returns the legacy sale or rejection message.

Risk:

- Medium risk.

Reason:

- It mutates only one character file.
- It already uses `get_potion_sell_value()` from `src.potion_repository`.
- It does not mutate `potions.json`.
- It still changes renown and inventory state, so it must be tested before extraction.

Recommendation:

- Possible first mutation target after read-only shop display is handled.
- Not the first overall target unless shop display proves unsuitable.

---

### `pri_10_usepotion`

Classification:

- Potion lifecycle mutation
- Temporary combat modifier setup
- Permanent character progression mutation
- Character-file mutation
- Combat-adjacent behavior

Behavior owned:

- Loads character sheet.
- Checks potion effect information.
- Applies permanent stat potion progression.
- Applies respec potion behavior.
- Applies stimulant potion behavior.
- Applies temporary next-match potion effects.
- Mutates potion effect fields such as `potionhit`, `potiondamage`, `potionac`, `potionstr`, `potiondex`, `potioncon`, `potionhp`, `potionblur`, and `potionregen`.
- Removes consumed potions from inventory.
- Writes the character file.

Risk:

- High risk.

Reason:

- This function mixes permanent progression, temporary combat setup, inventory removal, and potion lifecycle behavior.
- It touches fields later used by character view and combat.
- It has many legacy branches and legacy edge cases.

Recommendation:

- Do not touch during the first inventory/economy implementation pass.
- This needs its own dedicated potion lifecycle test plan later.

---

### `pri_11_givepotion`

Classification:

- Inventory transfer mutation
- Multi-character file mutation

Behavior owned:

- Loads the gifter character sheet.
- Loads the recipient character sheet.
- Checks whether the gifter owns the potion.
- Checks recipient potion inventory space.
- Removes the potion from the gifter.
- Adds the potion to the recipient.
- Writes both character files.
- Returns the legacy transfer or rejection message.

Risk:

- High risk.

Reason:

- This mutates two character files.
- Failed writes or partial mutations would be dangerous.
- Inventory capacity behavior must be preserved exactly.

Recommendation:

- Do not touch until single-character potion sale behavior is tested and stable.

---

### `pri_11_stockarmor`

Classification:

- Shop restock mutation
- Randomized shop generation
- Global data-file mutation

Behavior owned:

- Randomly generates 20 armor entries.
- Selects attributes from category-one, category-two, and category-three armor lists.
- Writes generated armor into the armor shop list.
- Writes `armor.json`.
- Returns a shop-stocked message.

Risk:

- Medium to high risk.

Reason:

- This does not mutate character files.
- It does mutate global armor shop data.
- It uses randomness and multi-category item construction.
- Current code should be inspected carefully before any refactor because it appears to rely on `armorDictionary` while assigning `armorData = get_armor_dictionary()`.

Recommendation:

- Do not extract first.
- Needs characterization tests with controlled randomness before refactor.

---

### `pri_10_armorshop`

Classification:

- Read-only shop/list display
- Armor price calculation
- Message construction

Behavior owned:

- Reads armor data through `get_armor_dictionary()`.
- Calculates armor prices from category data.
- Builds the displayed armor shop list.
- Returns the armor shop display string.

Risk:

- Low to medium risk.

Reason:

- This appears to be the safest next implementation candidate because it should only build display output.
- It does not appear intended to mutate character files or global armor data.
- However, it should be tested first because the current body uses `armorDictionary` after assigning `armorData`, so legacy behavior must be confirmed before any cleanup.

Recommendation:

- Best first implementation candidate if tests can capture current behavior.
- Start with legacy wrapper tests for `pri_10_armorshop()` before extracting any helper.

---

### `pri_9_buyarmor`

Classification:

- Purchase economy mutation
- Inventory mutation
- Global shop mutation
- Character-file mutation

Behavior owned:

- Loads armor data.
- Loads buyer character sheet.
- Validates selected armor.
- Rejects sold armor.
- Calculates armor price from category data.
- Checks buyer renown.
- Checks armor inventory capacity.
- Subtracts renown.
- Marks armor shop item as sold.
- Adds armor to the first available armor inventory slot.
- Appends price to the stored armor item.
- Writes the character file.
- Writes `armor.json`.

Risk:

- High risk.

Reason:

- This mutates both character data and global shop data.
- It changes renown and equipment inventory.
- It relies on armor list shape and stored sale-price behavior.
- It should not be touched before dedicated tests exist.

Recommendation:

- Not a first extraction target.

---

### `pri_10_sellarmor`

Classification:

- Sale economy mutation
- Equipment inventory mutation
- Character-file mutation

Behavior owned:

- Loads seller character sheet.
- Rejects missing character.
- Checks whether the requested armor key exists.
- Rejects selling currently equipped armor.
- Calculates sale value from stored purchase price.
- Adds renown to seller.
- Clears the armor slot.
- Attempts to normalize armor slot keys.
- Writes the character file.

Risk:

- High risk.

Reason:

- This changes renown and armor inventory state.
- It interacts with equipped armor protection.
- The key-normalization behavior is legacy-sensitive and should not be altered casually.

Recommendation:

- Do not touch until armor shop display and armor purchase behavior are fully tested.

---

### `pri_10_namearmor`

Classification:

- Equipment state mutation
- Armor inventory key mutation
- Character-file mutation

Behavior owned:

- Loads character sheet.
- Checks whether the old armor key exists.
- Rejects duplicate new armor names.
- Rejects renaming equipped armor.
- Renames the armor inventory key.
- Writes the character file.

Risk:

- High risk.

Reason:

- This changes dictionary keys used by equip, unequip, sell, and view behavior.
- It can affect equipment references.
- It should not be mixed into shop or economy extraction.

Recommendation:

- Defer to a later armor lifecycle pass.

---

### `pri_6_equip`

Classification:

- Equipment state mutation
- Combat-adjacent stat mutation
- Character-file mutation

Behavior owned:

- Loads character sheet.
- Rejects equip attempts during combat.
- Resets armor bonus fields.
- Sets `equip`.
- Reads armor category data.
- Applies armor stat bonuses to character fields.
- Mutates combat-facing fields such as `armorhit`, `armordamage`, `armorac`, `armorhp`, `armordr`, `armorinitiative`, `armorstrength`, `armordexterity`, `armorconstitution`, and `armorblur`.
- Writes the character file.

Risk:

- Very high risk.

Reason:

- This directly changes fields used by character view and combat.
- It is equipment lifecycle behavior, not simple inventory/economy behavior.
- It should not be touched until armor lifecycle tests exist.

Recommendation:

- Explicitly avoid for now.

---

### `pri_8_unequip`

Classification:

- Equipment state mutation
- Combat-adjacent stat mutation
- Character-file mutation

Behavior owned:

- Rejects unequip attempts during combat.
- Loads character sheet.
- Clears `equip`.
- Resets armor bonus fields.
- Writes the character file.

Risk:

- High risk.

Reason:

- Simpler than equip, but still changes combat-facing armor bonus fields.
- Must remain paired conceptually with equip behavior.
- Should not be extracted by itself unless the armor lifecycle pass deliberately starts there.

Recommendation:

- Defer to a later armor lifecycle pass.

---

## Initial Audit Conclusion

The safest next implementation candidate appears to be:

- `pri_10_armorshop`

Reason:

- It is the closest to read-only shop/list display behavior.
- It should not mutate character files.
- It should not mutate `armor.json`.
- It can likely be tested with fixed in-memory armor shop data.

However, before extracting anything, create characterization tests for the current legacy behavior.

The next implementation step should be:

- Add tests for `pri_10_armorshop()`.
- Use controlled armor list input.
- Preserve the current output format exactly.
- Do not import `botCommand.py`.
- Do not touch buying, selling, equipping, unequipping, potion use, potion transfer, or randomized shop restocking yet.

Status:

- Initial inventory/economy boundary review complete.
- First recommended implementation target: armor shop display only.

## Armor Shop Display Extraction

### Completed Work

The read-only armor shop display behavior was extracted from `original/onPRIUtils.py` into the armor repository layer.

Created:

- `calculate_armor_effect_price()` in `src.armor_repository`
- `calculate_armor_item_price()` in `src.armor_repository`
- `build_armor_shop_display()` in `src.armor_repository`

Legacy wrapper:

- `pri_10_armorshop()` now delegates armor shop display construction to `build_armor_shop_display()`.

Behavior preserved:

- Single-attribute armor display is preserved.
- Two-attribute armor display is preserved.
- Three-attribute armor display is preserved.
- Sold armor still displays with `0` renown.
- Multiple armor entries still display in the same newline-separated format.
- Legacy F-list color tags and output formatting are preserved.
- No character files are read or written.
- `armor.json` is not mutated by armor shop display.
- Buying, selling, naming, equipping, unequipping, and armor restocking behavior were not changed.

Tests added or expanded:

- `tests/test_armor_repository.py`
- `tests/test_legacy_onpriutils_armorshop.py`

Current full pytest result:

- `275 passed`

Status:

- Complete for read-only armor shop display extraction.

---

## Updated Inventory and Economy Position

The first safe inventory/economy extraction target is complete.

Remaining inventory/economy targets are no longer read-only display-only behavior. The next safest area should be selected carefully.

Possible next targets:

### Lower-to-Medium Risk

- `pri_11_sellpotion`

Reason:

- Mutates only one character file.
- Does not mutate `potions.json`.
- Already uses `get_potion_sell_value()` from `src.potion_repository`.
- Still changes renown and potion inventory, so it needs tests first.

### Medium-to-High Risk

- `pri_10_stockpotion`
- `pri_11_stockarmor`

Reason:

- Mutate global shop data.
- Use randomness.
- Need controlled randomness before extraction.

### High Risk

- `pri_10_buypotion`
- `pri_9_buyarmor`
- `pri_10_sellarmor`
- `pri_10_namearmor`
- `pri_6_equip`
- `pri_8_unequip`
- `pri_10_usepotion`
- `pri_11_givepotion`

Reason:

- Mutate persistent character state, global shop state, equipment state, combat-facing fields, or multiple character files.

Recommended next implementation target:

- `pri_11_sellpotion`

Reason:

- It is the smallest single-character economy mutation left.
- It already partially depends on `src.potion_repository`.
- It does not touch global shop stock.
- It can be covered with temporary character files and isolated tests before extraction.

Do not begin the next implementation until the audit update is committed.

## Potion Sale Extraction

### Completed Work

The single-character potion sale behavior was extracted from `original/onPRIUtils.py` into the potion repository layer.

Created:

- `sell_character_potion()` in `src.potion_repository`

Legacy wrapper:

- `pri_11_sellpotion()` now delegates deterministic potion sale logic to `sell_character_potion()`.

Behavior preserved:

- Owned potions can still be sold for half their listed potion value.
- The seller's renown is still increased by the half-price value.
- The sold potion is still removed from the seller's potion inventory.
- Missing potions still return the legacy rejection message.
- Potions missing from potion data still return the legacy unknown-potion message.
- Character file loading and saving remain in `original/onPRIUtils.py`.
- The legacy missing-character `UnboundLocalError` behavior is intentionally preserved and covered by test.
- Potion buying, potion use, potion transfer, potion restocking, armor buying, armor selling, armor naming, equipping, unequipping, combat behavior, XP payout, renown payout, and level-up handling were not changed.

Tests added or expanded:

- `tests/test_potion_repository.py`
- `tests/test_legacy_onpriutils_sellpotion.py`

Current full pytest result:

- `282 passed`

Status:

- Complete for single-character potion sale extraction.

---

## Updated Inventory and Economy Position

Completed inventory/economy extraction targets:

- Read-only armor shop display
- Single-character potion sale

Remaining targets should now be treated with higher caution.

Possible next targets:

### Medium Risk

- `pri_10_stockpotion`
- `pri_11_stockarmor`

Reason:

- They mutate global shop data.
- They use randomness.
- They do not mutate character files directly.
- They need controlled randomness tests before extraction.

### Medium-to-High Risk

- `pri_10_buypotion`

Reason:

- Mutates one character file and `potions.json`.
- Changes renown, potion inventory, and shop stock.
- Safer than potion use or potion transfer, but riskier than potion sale.

### High Risk

- `pri_9_buyarmor`
- `pri_10_sellarmor`
- `pri_10_namearmor`
- `pri_6_equip`
- `pri_8_unequip`
- `pri_10_usepotion`
- `pri_11_givepotion`

Reason:

- These mutate armor inventory, equipment keys, combat-facing fields, temporary potion effects, permanent character progression, or multiple character files.

Recommended next implementation target:

- `pri_10_stockpotion`

Reason:

- It is a global shop mutation, but it does not touch character files.
- It can be tested with controlled randomness.
- It is a better next target than potion buying because it avoids renown and character inventory mutation.
- It should be handled as a shop-restock extraction, not as potion lifecycle behavior.

Do not begin the next implementation until this audit update is committed.


## Potion Shop Restock Extraction

### Completed Work

The potion shop restock behavior was extracted from `original/onPRIUtils.py` into the potion repository layer.

Created:

- `stock_potion_shop()` in `src.potion_repository`

Legacy wrapper:

- `pri_10_stockpotion()` now delegates potion shop restock construction to `stock_potion_shop()` while keeping `potions.json` file writing in `original/onPRIUtils.py`.

Behavior preserved:

- Potion shop restocking still replaces the existing `shoplist`.
- The shop still receives 20 potion entries.
- Legacy rarity thresholds are preserved:
  - `98-100` selects relic potions.
  - `90-97` selects very rare potions.
  - `77-89` selects rare potions.
  - `51-76` selects uncommon potions.
  - `1-50` selects common potions.
- Legacy random index selection behavior is preserved.
- The returned shop string is preserved.
- The returned restock message is preserved.
- Character files are not read or written.
- Potion buying, potion selling, potion use, potion transfer, armor behavior, combat behavior, XP payout, renown payout, and level-up handling were not changed.

Additional cleanup:

- A duplicate earlier `pri_10_stockpotion()` definition was removed from `original/onPRIUtils.py`.
- The remaining active `pri_10_stockpotion()` definition is the delegated wrapper.

Tests added or expanded:

- `tests/test_potion_repository.py`
- `tests/test_legacy_onpriutils_stockpotion.py`

Current full pytest result:

- `286 passed`

Status:

- Complete for potion shop restock extraction.

---

## Updated Inventory and Economy Position

Completed inventory/economy extraction targets:

- Read-only armor shop display
- Single-character potion sale
- Potion shop restock

Remaining targets are higher risk because they mutate character inventory, global shop state, armor equipment state, combat-facing fields, multiple character files, or permanent progression state.

Possible next targets:

### Medium-to-High Risk

- `pri_10_buypotion`

Reason:

- Mutates one character file and `potions.json`.
- Changes renown, potion inventory, and shop stock.
- It is riskier than potion sale and potion shop restock, but still more contained than potion use or potion transfer.

### Medium-to-High Risk

- `pri_11_stockarmor`

Reason:

- Mutates global armor shop data.
- Uses randomness.
- Does not mutate character files directly.
- Needs controlled-randomness tests.
- Current code should be handled carefully because it historically mixed `armorData` and `armorDictionary`.

### High Risk

- `pri_9_buyarmor`
- `pri_10_sellarmor`
- `pri_10_namearmor`
- `pri_6_equip`
- `pri_8_unequip`
- `pri_10_usepotion`
- `pri_11_givepotion`

Reason:

- These mutate armor inventory, equipment keys, combat-facing fields, temporary potion effects, permanent character progression, or multiple character files.

Recommended next implementation target:

- `pri_10_buypotion`

Reason:

- It is the next smallest potion economy mutation.
- It is more useful than armor restocking because it continues the potion economy path already started.
- It can be tested with temporary character files and temporary `potions.json`.
- It should keep file I/O in the wrapper and move only deterministic purchase-state mutation into `src.potion_repository`.

Do not begin the next implementation until this audit update is committed.

## Potion Shop Restock Extraction

### Completed Work

The potion shop restock behavior was extracted from `original/onPRIUtils.py` into the potion repository layer.

Created:

- `stock_potion_shop()` in `src.potion_repository`

Legacy wrapper:

- `pri_10_stockpotion()` now delegates potion shop restock construction to `stock_potion_shop()` while keeping `potions.json` file writing in `original/onPRIUtils.py`.

Behavior preserved:

- Potion shop restocking still replaces the existing `shoplist`.
- The shop still receives 20 potion entries.
- Legacy rarity thresholds are preserved:
  - `98-100` selects relic potions.
  - `90-97` selects very rare potions.
  - `77-89` selects rare potions.
  - `51-76` selects uncommon potions.
  - `1-50` selects common potions.
- Legacy random index selection behavior is preserved.
- The returned shop string is preserved.
- The returned restock message is preserved.
- Character files are not read or written.
- Potion buying, potion selling, potion use, potion transfer, armor behavior, combat behavior, XP payout, renown payout, and level-up handling were not changed.

Additional cleanup:

- A duplicate earlier `pri_10_stockpotion()` definition was removed from `original/onPRIUtils.py`.
- The remaining active `pri_10_stockpotion()` definition is the delegated wrapper.

Tests added or expanded:

- `tests/test_potion_repository.py`
- `tests/test_legacy_onpriutils_stockpotion.py`

Current full pytest result:

- `286 passed`

Status:

- Complete for potion shop restock extraction.

---

## Updated Inventory and Economy Position

Completed inventory/economy extraction targets:

- Read-only armor shop display
- Single-character potion sale
- Potion shop restock

Remaining targets are higher risk because they mutate character inventory, global shop state, armor equipment state, combat-facing fields, multiple character files, or permanent progression state.

Possible next targets:

### Medium-to-High Risk

- `pri_10_buypotion`

Reason:

- Mutates one character file and `potions.json`.
- Changes renown, potion inventory, and shop stock.
- It is riskier than potion sale and potion shop restock, but still more contained than potion use or potion transfer.

### Medium-to-High Risk

- `pri_11_stockarmor`

Reason:

- Mutates global armor shop data.
- Uses randomness.
- Does not mutate character files directly.
- Needs controlled-randomness tests.
- Current code should be handled carefully because it historically mixed `armorData` and `armorDictionary`.

### High Risk

- `pri_9_buyarmor`
- `pri_10_sellarmor`
- `pri_10_namearmor`
- `pri_6_equip`
- `pri_8_unequip`
- `pri_10_usepotion`
- `pri_11_givepotion`

Reason:

- These mutate armor inventory, equipment keys, combat-facing fields, temporary potion effects, permanent character progression, or multiple character files.

Recommended next implementation target:

- `pri_10_buypotion`

Reason:

- It is the next smallest potion economy mutation.
- It is more useful than armor restocking because it continues the potion economy path already started.
- It can be tested with temporary character files and temporary `potions.json`.
- It should keep file I/O in the wrapper and move only deterministic purchase-state mutation into `src.potion_repository`.

Do not begin the next implementation until this audit update is committed.

## Potion Purchase Extraction

### Completed Work

The potion purchase behavior was extracted from `original/onPRIUtils.py` into the potion repository layer.

Created:

- `get_potion_price_from_data()` in `src.potion_repository`
- `buy_character_potion()` in `src.potion_repository`

Legacy wrapper:

- `pri_10_buypotion()` now delegates deterministic potion purchase-state mutation to `buy_character_potion()` while keeping file loading and saving in `original/onPRIUtils.py`.

Behavior preserved:

- Available potions can still be purchased from the current potion shop.
- The buyer's renown is still reduced by the potion price.
- Purchased potions are still added to the buyer's potion inventory.
- Purchased potions are still removed from `potions.json` shop stock.
- Potions not currently for sale still return the legacy rejection message.
- Buyers without enough renown still receive the legacy insufficient-renown message.
- Buyers with full potion inventories still receive the legacy inventory-space message.
- The legacy misspelling `puchased` is intentionally preserved.
- Character file loading and saving remain in `original/onPRIUtils.py`.
- `potions.json` loading and saving remain in `original/onPRIUtils.py`.
- Potion use, potion transfer, potion restocking, armor behavior, combat behavior, XP payout, renown payout, and level-up handling were not changed.

Tests added or expanded:

- `tests/test_potion_repository.py`
- `tests/test_legacy_onpriutils_buypotion.py`

Current full pytest result:

- `294 passed`

Status:

- Complete for potion purchase extraction.

---

## Updated Inventory and Economy Position

Completed inventory/economy extraction targets:

- Read-only armor shop display
- Single-character potion sale
- Potion shop restock
- Potion purchase

The main potion economy path now has repository-backed helpers for sale, restock, and purchase behavior.

Remaining targets are higher risk.

Possible next targets:

### Medium-to-High Risk

- `pri_11_stockarmor`

Reason:

- Mutates global armor shop data.
- Uses randomness.
- Does not mutate character files directly.
- Needs controlled-randomness tests.
- Current code should be handled carefully because it historically mixed `armorData` and `armorDictionary`.

### High Risk

- `pri_9_buyarmor`
- `pri_10_sellarmor`
- `pri_10_namearmor`
- `pri_6_equip`
- `pri_8_unequip`
- `pri_10_usepotion`
- `pri_11_givepotion`

Reason:

- These mutate armor inventory, equipment keys, combat-facing fields, temporary potion effects, permanent character progression, or multiple character files.

Recommended next implementation target:

- `pri_11_stockarmor`

Reason:

- It is the closest armor-side equivalent to the completed potion shop restock extraction.
- It mutates only global shop data, not character files.
- It can be tested with controlled randomness.
- It should be handled before armor buying, selling, naming, equipping, or unequipping.

Do not begin the next implementation until this audit update is committed.