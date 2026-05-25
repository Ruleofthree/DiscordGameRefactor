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