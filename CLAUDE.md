# Working Memory

## Project

**Autobahn nach 56** — HOI4 submod that merges Road to 56 tech with Kaiserreich.
Current goal: stabilize the full KR-centered playset on HOI4 1.18.x via staged isolation + targeted compatching.

## Terms

| Term | Meaning |
|------|---------|
| **KR** | Kaiserreich — main mod, source of truth for gameplay |
| **Autobahn** | Autobahn nach 56 — this repo (Workshop ID 2823622716) |
| **KNR** | Kaiserreich Naval Rework (Workshop ID 2862849828) |
| **RT56** | Road to 56 — base mod Autobahn is built upon |
| **KX** | KaiserRedux — alternative KR variant |
| **BM** | Better Mechanics — suite of optional modules |
| **ETD** | Expanded Tank Designer - Even More Fixed!+ (Workshop ID 3366131759) |
| **compatch** | Compatibility patch — the "Autobahn nach 56 and KNR Compatch" (Workshop ID 2990847665) |
| **2ACW** | Second American Civil War — KR gameplay chain (must work correctly) |
| **SPH** | Better Mechanics: Supply Production Health |
| **error.log** | Primary validation artifact at E:\Games\Paradox Interactive\Hearts of Iron IV\logs\error.log |

## Mod Stack (active mods in order)

1. Kaiserreich (1521695605)
2. Autobahn nach 56 (2823622716) — this repo
3. Kaiserreich Naval Rework (2862849828)
4. Autobahn<->KNR Compatch (2990847665) — stale, needs rebuild
5. KNR KR Runtime Fix — local submod in submods/knr_kr_runtime_fix/
6. [Various Better Mechanics modules — disabled in debug playset]
7. [Expanded Tank Designer — disabled in debug playset]
8. [Autobahn KR 2ACW Fix — likely obsolete]

## Key File Ownership Conflicts

| File | Winning Mod |
|------|------------|
| plane_airframes.txt | Autobahn (invalid idea spam: BUL, MPL, GER treaty) |
| tank_chassis.txt | Expanded Tank Designer (stale chassis/module assumptions) |
| countrytechtreeview.gui | Autobahn<->KNR Compatch (stale frozen merge) |
| 00_production.txt | Better Mechanics: AI Divisions (invalid techs/triggers) |
| special_forces_doctrine.txt | Autobahn (category drift) |

## Important Paths

| Path | Purpose |
|------|---------|
| E:\SteamLibrary\steamapps\common\Hearts of Iron IV | Game install |
| E:\Games\Paradox Interactive\Hearts of Iron IV | User data + logs |
| E:\SteamLibrary\steamapps\workshop\content\394360 | Workshop root |
| D:\Downloads\OneDrive\Documents\code\autobahn | This repo |
| D:\Downloads\OneDrive\Documents\code\knr-kr-runtime-fix | Related local source |

## Current Phase

**Phase 1** — building the KR Harmony Debug playset (minimal baseline).

Active decision: Phase 1 → if clean, Phase 3 is main work. If still noisy, Phase 2 seam repairs are the priority.

## Ground Rules

1. Kaiserreich is the source of truth for gameplay.
2. Surgical compatibility, not broad rewrites.
3. Multiple simultaneous failure sources — don't assume one mod is the problem.
4. No stale local shims kept alive just because they existed earlier.
5. Use effective file ownership + live logs, not workshop descriptions.

## Submodules in Repo

| Path | Status | Purpose |
|------|--------|---------|
| submods/knr_kr_runtime_fix/ | Active, needs 1.18 update | Fixes KNR has_navy_size scope, armoured cruiser equipment/project |
| submods/autobahn_kr_2acw_fix/ | Likely obsolete | Old 2ACW chain fix — test without it |
| submods/kr_tech_tree_fix/ | Unknown | Separate KR tech tree fix |
