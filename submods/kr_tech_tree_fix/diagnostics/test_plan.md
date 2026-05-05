# Test Plan

## Load order

1. Disable `Expanded Tank Designer - Even More Fixed!+`.
2. Add `KR Tech Tree Fix`.
3. Move `KR Tech Tree Fix` to the very end of the playset.

## Launch checks

1. Launch HOI4.
2. Confirm the main menu loads.
3. Start a new 1936 game.
4. Open the technology tree immediately.
5. Open the tank designer.
6. Open naval production if you want to confirm the FNG/KNR OOB typo is gone.

## Country smoke tests

1. USA or WCA
   - lets you hit the American Civil War tank-variant effects quickly
2. FRA or NFA
   - covers the logged French historical tank variants
3. FNG
   - covers the fixed auxiliary ship typo

## Runtime smoke

1. Let the game run for 7 to 14 days.
2. Save and quit.
3. Re-open `error.log`.

## PowerShell grep

```powershell
rg -n "Invalid tech|has_tech: Invalid tech|is not A valid Idea|Invalid module|create_equipment_variant|Undefined GUI_TYPE|Unexpected token|technology_sharing_offset|tank_chassis|plane_airframes|ship_deck_space" "D:\Downloads\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\logs\error.log"
```

## Expected result

- No `Undefined GUI_TYPE: technology_sharing_offset`
- No tank-variant spam caused by Expanded Tank Designer
- The `vnr_vnr_ship_hull_civilian_1` token should disappear
- Large `has_idea` floods for the dummy idea keys should disappear
- Remaining naval module errors, if any, should be limited to the broader KNR carrier/deck seam
