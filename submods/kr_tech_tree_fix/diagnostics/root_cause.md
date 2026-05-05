# Root Cause

## Primary break

`Expanded Tank Designer - Even More Fixed!+` is the primary incompatible mod in this stack.

Verified ownership:

- It wins `common/units/equipment/tank_chassis.txt`.
- It wins `interface/tank_designer_view.gui`.
- It wins `common/technologies/NSB_armor.txt`.

Verified mismatch:

- Kaiserreich and Autobahn tank variants still assume the vanilla/KR chassis slot schema where `special_type_slot_1` can hold radios, special modules, or secondary turrets.
- Expanded Tank Designer rewires the live schema so `special_type_slot_1` is radio-only and moves hull modifications into a dedicated `special_type_slot_6`.
- Live errors match that exact file-level mismatch:
  - `M1 Combat Car` uses `special_type_slot_1 = additional_machine_guns`.
  - `FCM 36` uses `special_type_slot_2 = sloped_armor`.
  - `T-28` uses `special_type_slot_1 = secondary_turret_hmg`.
- Those module placements are valid in vanilla/KR but invalid against Expanded Tank Designer's winning chassis file.

Result:

- The mod cannot be treated as a small reference typo.
- Keeping it active would require a wide merge across tank chassis, module categories, historical variants, scripted variant spawners, and the custom tank GUI.
- That is too invasive for a safe compatibility patch.

## Secondary stack seams

These are separate from the primary tank-designer incompatibility and are safe to patch locally:

1. `Autobahn nach 56` wins `interface/countrytechnologyview.gui` but omits the vanilla `technology_sharing_offset` position type.
2. `Autobahn nach 56` wins `common/technologies/industry.txt` and calls `FIN_nokia_tires_after_tech_effect`, which is missing in the active stack. That parser failure occurs before the rubber-processing tech definitions, which then causes downstream `Invalid technology: rubber_processing` errors.
3. `Kaiserreich Naval Rework` ships `history/units/00_kr_FNG_naval.txt` with a typo:
   - `vnr_vnr_ship_hull_civilian_1`
   - the actual defined hull is `vnr_ship_hull_civilian_1`
4. The user preset file [newb.txt](/D:/Downloads/OneDrive/Documents/Paradox%20Interactive/Hearts%20of%20Iron%20IV/game%20rules/newb.txt:1) contains `vnr_ai_naval_management`, which no active mod defines.
