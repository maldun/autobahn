# Remaining Risks

## Required user action

- `Expanded Tank Designer - Even More Fixed!+` should be disabled.
  - This patch does not override its tank chassis or tank GUI.
  - If it remains enabled, historical KR/Autobahn tank variants will continue to fail because the winning slot schema is still incompatible.

## Known unresolved seams

- Carrier and deck-module variant errors from `Kaiserreich Naval Rework` still need a separate focused merge if you want a fully clean naval log.
  - Examples include `ship_deck_space` and `ship_armor_carrier_deck` slot/category mismatches in focus-spawned ship variants.
  - These are outside the technology-tree break and were already documented in the local KNR runtime-fix README as a broader unresolved naval seam.

- The user preset [newb.txt](/D:/Downloads/OneDrive/Documents/Paradox%20Interactive/Hearts%20of%20Iron%20IV/game%20rules/newb.txt:1) has already been backed up and cleaned.
  - Backup: [newb.txt.bak-20260504-161356](</D:/Downloads/OneDrive/Documents/Paradox Interactive/Hearts of Iron IV/game rules/newb.txt.bak-20260504-161356>)
  - If you restore that backup later, the obsolete `vnr_ai_naval_management` parser error will return.

- Additional doctrine and Better Mechanics parser warnings remain in this playset.
  - They appear unrelated to the tank-tech-tree break addressed here.
  - Examples from the current log include doctrine unexpected-token warnings and Better Mechanics name/GUI parser warnings.
