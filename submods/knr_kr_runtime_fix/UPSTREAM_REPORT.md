# KNR Upstream Report

## Summary

This report isolates `Kaiserreich Naval Rework` issues that are reproducible against `Kaiserreich` and are not just generic launcher or UI noise.

The most important confirmed KNR/KR compatibility problems are:

1. KNR naval admiral traits evaluate `has_navy_size` in `Character` scope.
2. KNR does not provide KR's renamed `ship_hull_armoured_cruiser` equipment type.
3. KR's `sp_naval_armoured_cruiser` seam is missing at runtime in the tested stack unless it is re-added explicitly.
4. KNR's `no_old_navy_production` AI strategy has an empty `enable` block and throws a parser warning.

## Confirmed KNR-owned defects

### 1. Invalid-scope admiral traits

File:

- `common/unit_leader/01_vnr_naval_traits.txt`

Affected traits:

- `concealment_expert`
- `lone_wolf`
- `smoke_screen_expert`
- `hunter_killer`
- `marksman`
- `crisis_magician`

Problem:

- each trait calls `has_navy_size = { size > 50 }` inside `ai_will_do`
- HOI4 logs this as `Invalid Scope, supported: Country, provided: Character`

Observed log signature:

- `common/unit_leader/01_vnr_naval_traits.txt:100: has_navy_size: Invalid Scope, supported: Country, provided: Character`

Patch approach:

- keep the traits intact
- move the fleet-size check through `owner = { has_navy_size = { size > 50 } }`

### 2. Missing KR armoured-cruiser equipment type

KR renamed:

- `ship_hull_cruiser_panzerschiff` -> `ship_hull_armoured_cruiser`

KNR currently keeps:

- `vnr_ship_hull_cruiser_panzerschiff`

but does not define:

- `ship_hull_armoured_cruiser`

Impact:

- KR scripted effects, history units, focuses, decisions, and special projects that refer to `ship_hull_armoured_cruiser` fail
- German/GEA `Admiral Scheer Class` content is one visible casualty

Observed pre-patch log signatures:

- `invalid database object for effect/trigger ... ship_hull_armoured_cruiser`
- `sp:sp_naval_armoured_cruiser does not match any Special Project in database`
- `create_equipment_variant ... Admiral Scheer Class` failures

Patch approach:

- add a KR-compat `ship_hull_armoured_cruiser` definition that uses KNR's live panzerschiff slot layout, not old KR stats

### 3. Armoured-cruiser special-project seam missing

File seam:

- KR expects `sp_naval_armoured_cruiser`

Observed pre-patch log signature:

- `sp:sp_naval_armoured_cruiser does not match any Special Project in database`

Patch approach:

- re-add `sp_naval_armoured_cruiser`
- keep its outputs targeted at `ship_hull_armoured_cruiser`

### 4. Empty-enable AI strategy warning

File:

- `common/ai_strategy/naval_production.txt`

Problem:

- `no_old_navy_production` uses `enable = {}` with no conditions

Observed log signature:

- `AI strategy no_old_navy_production with missing or empty enable trigger`

Recommended upstream fix:

- change it to `enable = { always = yes }`

This was not included in the narrow local patch because silencing the warning cleanly requires a same-relative-path override of KNR's full `naval_production.txt`.

## Local patch contents

Files in this submod:

- `common/unit_leader/zz_knr_kr_naval_traits_compat.txt`
- `common/units/equipment/zz_knr_kr_armoured_cruiser_compat.txt`
- `common/special_projects/projects/zz_knr_kr_armoured_cruiser_project.txt`

## What the local startup test fixed

On the corrected second startup pass, these KNR/KR errors were gone:

- no `has_navy_size: Invalid Scope` from `01_vnr_naval_traits.txt`
- no `invalid database object ... ship_hull_armoured_cruiser`
- no `sp:sp_naval_armoured_cruiser does not match any Special Project`
- no `Admiral Scheer Class` slot-assignment failures

## Residual warnings that are not good upstream KNR targets

The tested playset still has heavy `script_enum_equipment_bonus_type` drift from other later-loading mods, especially Better Mechanics and other tech/project extensions.

Examples:

- `bm_transport_helicopter_equipment_1 not in script_enum_equipment_bonus_type`
- `armored_car not in script_enum_equipment_bonus_type`
- `support_ship is an equipment type or equipment category but is not in script enum`

These should be kept separate from the core KNR/KR report so the KNR author gets a clear defect list they can act on.

## Suggested message to the author

I traced a few real KNR compatibility issues against current Kaiserreich and built a minimal repro patch for them.

Confirmed KNR-owned problems:

1. `common/unit_leader/01_vnr_naval_traits.txt`
   The naval traits `concealment_expert`, `lone_wolf`, `smoke_screen_expert`, `hunter_killer`, `marksman`, and `crisis_magician` use `has_navy_size` in character scope. HOI4 logs `Invalid Scope, supported: Country, provided: Character`.

2. KNR does not define KR's renamed `ship_hull_armoured_cruiser`.
   KR still references that type in scripted effects, history units, decisions, focuses, and special projects, which breaks things like the German/GEA `Admiral Scheer Class` seam.

3. `sp_naval_armoured_cruiser` is missing at runtime in the tested stack unless it is re-added explicitly.

4. `common/ai_strategy/naval_production.txt`
   `no_old_navy_production` has an empty `enable = {}` block and throws the parser warning about a missing or empty enable trigger.

I built a minimal local patch for the first three items and verified on startup that it removes:

- the invalid-scope naval trait errors
- the missing `ship_hull_armoured_cruiser` database errors
- the missing `sp_naval_armoured_cruiser` errors
- the `Admiral Scheer Class` slot-assignment failures

The remaining startup enum spam in my full playset mostly comes from other mods overriding `script_enums.txt`, so I kept that separate from the KNR report.
