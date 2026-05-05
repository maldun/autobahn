# Tech Tree Fix Plan
## Full Log Analysis — HOI4 1.18.x + KR Playset

Generated from: `E:\Games\Paradox Interactive\Hearts of Iron IV\logs\error.log` (20,676 lines)
Date: 2026-05-05

---

## Root Cause Summary

The tech tree break is caused by **three Autobahn-owned files that have not been updated for HOI4 1.18**:

| Priority | File | Problem | Symptom |
|----------|------|---------|---------|
| **CRITICAL** | `interface/countrytechtreeview.gui` | Missing `rangers_tech_tree` gridboxtype (KR 1.18 added Rangers branch) | "Found no grid box for tech special_forces_rangers" × 9 every time tech tree opens |
| **CRITICAL** | `interface/countrydoctrinetreeview.gui` | Missing `special_forces_doctrine_folder_no_aat` container (HOI4 1.18 addition) | "Could not find special_forces_doctrine_folder_no_aat in window countrydoctrineview" |
| **HIGH** | `gfx/interface/equipmentdesigner/graphic_db/00_plane_icons.txt` (+ 3 others) | HOI4 1.18 changed how country-specific graphic_db blocks are parsed; old `TAG = {}` selector format rejected | "Expected 'default', a continent name or a country tag: SOV" × thousands; aircraft designer broken |

---

## Error Family Breakdown

### Family 1 — countrytechtreeview.gui missing Rangers gridbox (lines 20648–20668)
**Owner:** Autobahn  
**File:** `interface/countrytechtreeview.gui`

KR 1.18 added a `rangers_tech_tree` gridboxtype to its version of `countrytechtreeview.gui` (KR workshop line 302–307). Autobahn's file overrides this but was last updated before KR added Rangers. Result: the engine finds no container to render the Rangers tech branch.

```
# In KR's file (workshop 1521695605):
gridboxtype = {
    name = "rangers_tech_tree"
    position = { x = 140 y = 1110 }
    slotsize = { width = 70 height = 70 }
    format = "LEFT"
}
```

Autobahn's file has `paratroopers_tree` then `tech_special_forces_tree` with nothing in between.

**Fix:** Add `rangers_tech_tree` gridboxtype between `paratroopers_tree` and `tech_special_forces_tree` in Autobahn's file. ✅ APPLIED

**Techs affected (all show "Found no grid box"):**
- special_forces_rangers
- rangers_jaegers_training
- rangers_jungle_training
- rangers_guerilla_doctrine
- rangers_recon_terrain_training
- rangers_fire_support_integration
- rangers_urban_combat
- elite_rangers_doctrine
- rangers_backbone_doctrine

---

### Family 2 — countrydoctrinetreeview.gui missing no_aat folder (lines 20657, 20668)
**Owner:** Autobahn  
**File:** `interface/countrydoctrinetreeview.gui`

HOI4 1.18 vanilla added `special_forces_doctrine_folder_no_aat` — a Rangers-only doctrine folder used when AAT unit types are absent. Autobahn's file (1,310 lines) is a large RT56-merged override of the vanilla file but was frozen before 1.18 added this container window. The vanilla 1.18 file defines it at lines 19–86.

**Fix:** Insert `special_forces_doctrine_folder_no_aat` container window before `special_forces_doctrine_folder` in Autobahn's file. ✅ APPLIED

---

### Family 3 — Graphic DB format change (lines 2006–3645, ~1,600 errors)
**Owner:** Autobahn  
**Files:**
- `gfx/interface/equipmentdesigner/graphic_db/00_plane_icons.txt`
- `gfx/interface/equipmentdesigner/graphic_db/00_tank_icons.txt`
- `gfx/interface/equipmentdesigner/graphic_db/00_r56_dlc_tank_icons.txt`
- `gfx/interface/equipmentdesigner/graphic_db/01_bba_plane_icons.txt`

HOI4 1.18 changed the equipment graphic database format. The old format used raw country tags as block selectors (`SOV = { ... }`). In 1.18, only `default`, continent names, and a restricted set of vanilla tags are valid selectors. KR-specific tags like `SOV` (replaced in KR), `DDR`, `CSA`, `ISR`, `RUT`, etc. are rejected.

Additionally, `has_cosmetic_tag` is no longer valid inside graphic_db entries in 1.18 (invalid scope — Country expected, None provided).

**Sub-errors:**
- `Expected 'default', a continent name or a country tag: SOV` (and DDR, SPR, CSA, YUG, PRC, CAN, ISR, RUT, VNZ, OTT, etc.)
- `has_cosmetic_tag: Invalid Scope, supported: Country, provided: None` (thousands)
- `GFX referenced in equipment graphic database does not exist` — hundreds of missing GFX entries
- `Entity referenced in equipment graphic database does not exist` — hundreds of missing 3D entities
- `Unknown equipment type: supersonic_fighter_equipment_1` — RT56 equipment not in KR

**Fix (Phase 2D):**
- Rewrite country-specific blocks to use `default = { ... }` or valid continent groupings
- Remove all `has_cosmetic_tag` conditional triggers from graphic_db entries
- Audit `supersonic_fighter_equipment_1` — if no KR equivalent, remove the block

**Status:** PENDING

---

### Family 4 — plane_airframes.txt invalid ideas (lines 18000–20559, ~500+ hits per session)
**Owner:** Autobahn  
**File:** `common/units/equipment/plane_airframes.txt`

The file checks for ideas that don't exist in KR:
- `BUL_army_restrictions` (lines 6, 1527)
- `MPL_mandate` (lines 7, 1528)
- `GER_treaty_of_versailles` (line 8, 1529)
- `GER_treaty_of_versailles_2` (lines 9, 1530)
- `GER_treaty_of_versailles_3` (lines 10, 1531, 859)

Also: `tank_chassis.txt` references `BUL_army_restrictions` (lines 15, 339, 650).

**Fix (Phase 2D):**
```
# Remove or guard each check:
# Old: limit = { has_idea = BUL_army_restrictions }
# New: remove the limit entirely, or check for KR-equivalent idea
```

**Status:** PENDING

---

### Family 5 — aut56_tech on_actions country scope errors (lines 10026–10053)
**Owner:** Autobahn  
**Files:** `common/on_actions/*_aut56_tech.txt` (264 files)

HOI4 1.18 tightened validation of `on_startup` effects. The pattern:
```
on_startup = {
    effect = {
        ALO = {  # Direct country tag scope
            set_technology = { ... }
        }
    }
}
```
...now reports "Invalid effect 'ALO'" at parse time for non-vanilla or unregistered tags.

Affected countries include: ALO, CSA, INR, PSA, SIB, SQI, TEX, TRM, XXA (and ~255 more).

**Fix (Phase 2D):**
```
on_startup = {
    effect = {
        every_country = {
            limit = { tag = ALO }
            set_technology = { ... }
        }
    }
}
```

**Status:** PENDING — requires bulk sed/script across 264 files.

---

### Family 6 — BOM in r56_equip_air.gfx (line 25)
**Owner:** Autobahn  
**File:** `interface/r56_equip_air.gfx`

UTF-8 BOM byte sequence at file start causes parse failure: `Unexpected token: ﻿SpriteTypes`

**Fix (Phase 2D):** Strip BOM. One-line fix.

**Status:** PENDING

---

### Family 7 — Division names invalid tokens (lines 3645–~7500, ~2,000+ errors)
**Owner:** Autobahn (RT56-heritage files)  
**Files:** `common/units/names_divisions/*.txt` (all country files)

Two problems:
1. `division_types has unknown token: anti-air` / `anti-tank` — these RT56 division types were removed from KR's unit definitions. All country division name files referencing them fail.
2. `There is unknown tag in for_countries scope: KUW, UAE, DJI, WES, RIF, BAN, etc.` — KR-specific country tags in `for_countries` scope fail because 1.18 validates tags more strictly

**Fix (Phase 2D):**
- Remove `anti-air` and `anti-tank` from `division_types` in all names_divisions files
- The `for_countries` tag errors likely self-resolve when load order is correct; confirm first

**Status:** PENDING

---

### Family 8 — sov_tanks.txt SOV scope errors (lines 10000–10025)
**Owner:** Autobahn (RT56-heritage, RT56's `events/sov_tanks.txt`)  
**File:** `events/sov_tanks.txt`

RT56 carries Soviet tank events that reference `SOV = {}` scope. In KR, `SOV` doesn't exist as a country. Events never fire but generate load-time errors.

**Fix (Phase 2D):** Remove or stub `events/sov_tanks.txt` from Autobahn — these events are irrelevant in KR.

**Status:** PENDING

---

## Issues NOT Owned by Autobahn (Upstream)

| File | Owner | Error | Notes |
|------|-------|-------|-------|
| `common/scripted_effects/_add_starting_tech.txt:616` | KNR (2862849828) | `set_technology: vnr_less_fuel_consumption` invalid tech | KNR bug; report upstream |
| `common/on_actions/BM_supplyhealth_on_actions.txt` | BM | SOV/PRC/is_literally_china errors | BM compatibility gap |
| `common/special_projects/projects/BM_mobile_dockyard_project.txt:30` | BM | `has_tech: Invalid tech` — polling ~1/sec | Critical BM bug; disable BM or report |
| `common/scripted_effects/_00_Naval_Rework_Variants.txt` | KNR | Invalid name groups, unresolved hull types | KNR update needed |
| `[database_scoped_variables]` spam | KR/KNR | 1.18 variable validation tightening | Upstream mods' problem |
| `interface/gui.cpp:931` `technology_sharing_offset` | KR or vanilla | GUI_TYPE undefined — may crash | Investigate; possibly KR/compatch |

---

## Fix Priority Order

### Do now (Autobahn GUI files — surgical, low risk):
1. ✅ `countrytechtreeview.gui` — add `rangers_tech_tree` gridboxtype
2. ✅ `countrydoctrinetreeview.gui` — add `special_forces_doctrine_folder_no_aat`

### Phase 2D batch (Autobahn core repairs):
3. Fix `plane_airframes.txt` invalid idea checks (5 ideas at 6 line locations)
4. Strip BOM from `r56_equip_air.gfx`
5. Bulk-fix 264 `*_aut56_tech.txt` on_actions files (scripted refactor)
6. Update graphic_db files to 1.18 format (complex — rewrite country selector blocks)
7. Remove/stub `events/sov_tanks.txt`
8. Remove `anti-air`/`anti-tank` from division names files (bulk)

### Phase 2B (compatch rebuild — separate work):
9. Rebuild `x_plane_airframes.txt` (3-way merge: KR + Autobahn + KNR)
10. Rebuild `countrytechtreeview.gui` compatch layer (after Autobahn fixes settle)

### Phase 2C (KNR runtime fix update):
11. Confirm `knr_kr_runtime_fix` covers `vnr_less_fuel_consumption` issue in KNR
12. Bump KNR runtime fix to 0.2.0 + update descriptor to 1.18.*

---

## Expected State After GUI Fixes

After applying the two critical GUI fixes (items 1 and 2 above):
- `Found no grid box for tech special_forces_rangers` errors → eliminated
- `Could not find special_forces_doctrine_folder_no_aat` errors → eliminated
- The Rangers doctrine branch will render in the tech tree UI
- The special forces doctrine view will open without errors

Remaining visible breakage after those fixes: graphic_db errors (aircraft designer cosmetics), idea spam from plane_airframes.txt (does not block gameplay), BM polling spam.
