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