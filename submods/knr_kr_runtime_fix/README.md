# KNR KR Runtime Fix

This submod is a narrow compatibility patch for `Kaiserreich Naval Rework` on top of `Kaiserreich`.

## Scope

The first patch set only fixes seams that were confirmed by direct file tracing plus live `error.log` output:

- KNR naval admiral traits using `has_navy_size` in `Character` scope
- KNR not defining KR's renamed `ship_hull_armoured_cruiser` equipment type
- KNR not exposing KR's `sp_naval_armoured_cruiser` special project at runtime

## Confirmed issues

1. `common/unit_leader/01_vnr_naval_traits.txt`
   - Six naval traits call `has_navy_size` directly inside `ai_will_do`.
   - `error.log` reports `Invalid Scope, supported: Country, provided: Character`.
   - This matches the crash seam seen when clicking ghost admirals during KNR's pre-war US navy redistribution.

2. `common/units/equipment/ship_hull_cruiser.txt`
   - KNR keeps `vnr_ship_hull_cruiser_panzerschiff` but does not define KR's renamed `ship_hull_armoured_cruiser`.
   - KR still references `ship_hull_armoured_cruiser` in focus, decision, history-unit, scripted-effect, and special-project content.
   - This produces invalid database object errors, missing `Admiral Scheer Class` variants, and event/OOB ship spawn failures.

3. `common/special_projects/projects`
   - Live logs show `sp_naval_armoured_cruiser` missing from the database even though KR expects it.
   - This patch re-adds the project explicitly to keep the seam stable regardless of load-order quirks.

4. `common/ai_strategy/naval_production.txt`
   - `no_old_navy_production` has an empty `enable = {}` block.
   - Live logs flag this as a scripting mistake.
   - This is confirmed, but not patched in `0.1.0` because removing the parser warning cleanly requires a same-relative-path override of KNR's full `naval_production.txt`.

## Deliberately deferred

These seams were confirmed during the audit but are not patched in `0.1.0` because they need a wider merge or a runtime repro before changing them safely:

- KNR carrier AI design mismatches against the active `generic_naval.txt` carrier slots
- KNR `vnr_ship_hull_cruiser_submarine` equipment-bonus enum drift in special projects
- KNR's parse-time `no_old_navy_production` warning
- support/repair ship file drift from KR
- broader AI-navy behavioral complaints without a reproducible parser/runtime trace beyond the carrier design mismatch

## Files added

- `common/unit_leader/zz_knr_kr_naval_traits_compat.txt`
- `common/units/equipment/zz_knr_kr_armoured_cruiser_compat.txt`
- `common/special_projects/projects/zz_knr_kr_armoured_cruiser_project.txt`

## Test plan

Static checks:

- confirm `error.log` no longer reports `has_navy_size: Invalid Scope` from `01_vnr_naval_traits.txt`
- confirm `error.log` no longer reports `ship_hull_armoured_cruiser` as an invalid database object
- confirm `error.log` no longer reports `sp:sp_naval_armoured_cruiser does not match any Special Project in database`

In-game smoke tests:

1. Launch `Kaiserreich + KNR + this patch`.
2. Start a 1936 game and reach the US pre-war navy redistribution seam.
3. Click surviving US admiral/task-force shells during the collapsed-fleet state and verify no crash.
4. Start as or tag-switch to a country that uses KR armoured cruisers, such as GEA or GER.
5. Confirm ships using `ship_hull_armoured_cruiser` spawn correctly and KR naval events/focuses do not log missing equipment/project errors.
