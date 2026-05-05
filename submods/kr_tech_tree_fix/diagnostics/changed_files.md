# Changed Files

- `descriptor.mod`
  - Declares the local compatibility patch mod metadata.

- `../kr_tech_tree_fix.mod`
  - Launcher descriptor for installation into the HOI4 user mod directory.

- `interface/zz_kr_tech_tree_fix.gui`
  - Reintroduces `technology_sharing_offset` and `technology_sharing_faction_offset` so the research/technology view stops throwing undefined GUI type errors.

- `common/scripted_effects/zz_kr_tech_tree_fix_runtime_stubs.txt`
  - Adds empty scripted-effect stubs for missing callback names that were aborting technology-file parsing.
  - `FIN_nokia_tires_after_tech_effect` is required for the active Autobahn `industry.txt`.
  - The `ITA_add_*` stubs are defensive cleanup only; they do not make Expanded Tank Designer compatible.

- `common/ideas/zz_kr_tech_tree_fix_dummy_ideas.txt`
  - Adds harmless dummy ideas for missing idea keys that are spammed by the active Autobahn/KR/Better Mechanics stack.
  - This preserves current gameplay behavior because the patch does not grant those ideas to any country.

- `history/units/00_kr_FNG_naval.txt`
  - Overrides KNR's FNG OOB with a one-token hull-name typo fix so the auxiliary ship entry parses.

- `diagnostics/root_cause.md`
  - Documents the verified root-cause chain.

- `diagnostics/changed_files.md`
  - Tracks patch contents and rationale.

- `diagnostics/remaining_risks.md`
  - Lists unresolved conflicts and why they were left alone.

- `diagnostics/test_plan.md`
  - Provides the recommended validation sequence and log-grep command.

## Installed outside workspace

- `D:\Downloads\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod\kr_tech_tree_fix\...`
  - Installed copy of this patch bundle in the real HOI4 user mod directory.

- `D:\Downloads\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\mod\kr_tech_tree_fix.mod`
  - Installed launcher descriptor for the real HOI4 user mod directory.

- `D:\Downloads\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\game rules\newb.txt`
  - Backed up, then removed the stale `vnr_ai_naval_management` rule entry that no active mod now defines.

- `D:\Downloads\OneDrive\Documents\Paradox Interactive\Hearts of Iron IV\game rules\newb.txt.bak-20260504-161356`
  - Timestamped rollback backup created before editing `newb.txt`.
